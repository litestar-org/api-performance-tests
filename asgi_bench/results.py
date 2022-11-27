import json
from pathlib import Path

import pandas as pd
import plotly.express as px

from .spec import ENDPOINT_CATEGORIES
from .types import BenchmarkMode, SuiteResults
from .util import get_error_percentage

COLOR_PALETTE = [
    "#a78bfa",
    "#c8c9c5",
    "#2dd4bf",
    "#fb7185",
    "#c084fc",
    "#a78bfa",
    "#818cf8",
    "#60a5fa",
    "#38bdf8",
    "#22d3ee",
    "#2dd4bf",
    "#34d399",
    "#a3e635",
    "#facc15",
    "#fbbf24",
    "#fb923c",
    "#f87171",
    "#a8a29e",
    "#a1a1aa",
]


def get_numbered_runs(results_dir: Path) -> dict[int, Path]:
    return {int(file.stem.split("_")[-1]): file for file in results_dir.glob("run_*.json")}


def init_results_file(results_dir: Path) -> Path:
    results_dir.mkdir(exist_ok=True)
    numbered_runs = get_numbered_runs(results_dir)
    run_number = max(numbered_runs) + 1 if numbered_runs else 1
    return results_dir / f"run_{run_number}.json"


def collect_results(run_number: int | None = None) -> tuple[int, dict[str, SuiteResults]]:
    results_dir = Path.cwd() / "results"

    numbered_runs = get_numbered_runs(results_dir)
    if run_number is None:
        run_number = max(numbered_runs)

    results_file = numbered_runs[run_number]
    data: dict[str, SuiteResults] = json.loads(results_file.read_text())
    return run_number, data


def _data_for_plot(
    results: dict[str, SuiteResults],
    benchmark_mode: BenchmarkMode,
    tolerance: float,
    percentiles: tuple[str, ...],
    frameworks: tuple[str, ...] | None,
) -> pd.DataFrame | None:
    ret = []
    for framework, framework_results in results.items():
        if frameworks and framework not in frameworks:
            continue

        for endpoint_mode, endpoint_mode_results in framework_results[benchmark_mode].items():
            for category, category_results in endpoint_mode_results.items():  # type: ignore[attr-defined]
                for test_result in category_results:
                    error_percentage = get_error_percentage(test_result)
                    is_valid = error_percentage <= tolerance
                    for percentile in percentiles:
                        ret.append(
                            {
                                "target": framework,
                                "name": test_result["name"],
                                "endpoint_mode": endpoint_mode,
                                "category": category,
                                "stddev": test_result[benchmark_mode]["stddev"] if is_valid else 0,
                                "mean": test_result[benchmark_mode]["mean"] if is_valid else 0,
                                "score": test_result[benchmark_mode]["percentiles"][percentile] if is_valid else 0,
                                "percentile": percentile,
                            }
                        )

    if ret:
        data = sorted(ret, key=lambda r: r["target"])
        df = pd.DataFrame(data)
        return df

    return None


def _draw_plot(
    *,
    df: pd.DataFrame,
    output_dir: Path,
    benchmark_mode: BenchmarkMode,
    formats: tuple[str, ...],
    error_bars: bool,
    category: str | None = None,
    percentile: str | None = None,
):

    if benchmark_mode == "rps":
        title = "Requests per second (higher is better)"
    else:
        title = "Latency (lower is better)"

    df = df.query(f"category == '{category}'")

    if percentile:
        df = df.query(f"percentile == '{percentile}'")
        percentile_count = 1
    else:
        percentile_count = len(df["percentile"].unique())
    if df.empty:
        return

    plot = px.bar(
        df,
        x="name",
        y="score",
        color="target",
        barmode="group",
        text="target",
        title=title,
        facet_col="endpoint_mode",
        facet_row="percentile",
        height=280 * percentile_count if percentile_count > 1 else None,
        width=600 if percentile_count > 1 else None,
        labels={"score": "RPS", "endpoint_mode": "mode", "name": ""},
        # hover_data=["stddev"],
        # color_discrete_map={target: COLOR_PALETTE[i] for i, target in enumerate(df["target"].unique())},
    )

    for format_ in formats:
        filename_parts: list[str] = [benchmark_mode]
        if percentile:
            filename_parts.append(percentile)
        if category:
            filename_parts.append(category)
        filename = output_dir / Path("_".join(filename_parts)).with_suffix("." + format_)
        if format_ == "html":
            plot.write_html(filename)
        else:
            plot.write_image(filename, scale=2)


def make_plots(
    *,
    percentiles: tuple[str, ...],
    error_bars: bool,
    run_number: int | None,
    formats: tuple[str, ...] = ("png",),
    split_percentiles: bool,
    tolerance: float = 0.1,
    frameworks: tuple[str, ...] | None,
) -> None:
    cwd = Path.cwd()
    run_number, results = collect_results(run_number)
    output_dir = cwd / "plots" / f"run_{run_number}"
    output_dir.mkdir(exist_ok=True, parents=True)

    benchmark_modes: tuple[BenchmarkMode, ...] = ("rps", "latency")

    for benchmark_mode in benchmark_modes:
        if not all(benchmark_mode in mode_results for mode_results in results.values()):
            continue
        df = _data_for_plot(
            results, benchmark_mode, tolerance=tolerance, percentiles=percentiles, frameworks=frameworks
        )
        for category in ENDPOINT_CATEGORIES:
            if split_percentiles:
                for percentile in percentiles:
                    _draw_plot(
                        df=df,
                        output_dir=output_dir,
                        benchmark_mode=benchmark_mode,
                        formats=formats,
                        error_bars=error_bars,
                        category=category,
                        percentile=percentile,
                    )
            else:
                _draw_plot(
                    df=df,
                    output_dir=output_dir,
                    benchmark_mode=benchmark_mode,
                    formats=formats,
                    error_bars=error_bars,
                    category=category,
                )
