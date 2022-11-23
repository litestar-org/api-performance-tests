import json
from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from .spec import ENDPOINT_CATEGORIES
from .types import BenchmarkMode, EndpointCategory, SuiteResults
from .util import get_error_percentage

COLOR_PALETTE = [
    "#5C80BC",
    "#30323D",
    "#c8c9c5",
    "#2dd4bf",
    "#a78bfa",
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
    categories: tuple[EndpointCategory, ...] | EndpointCategory,
) -> pd.DataFrame | None:
    ret = []
    if isinstance(categories, str):
        categories = (categories,)
    for framework, framework_results in results.items():
        for endpoint_mode, endpoint_mode_results in framework_results[benchmark_mode].items():
            for category, category_results in endpoint_mode_results.items():  # type: ignore[attr-defined]
                if category not in categories:
                    continue
                for test_result in category_results:
                    error_percentage = get_error_percentage(test_result)
                    is_valid = error_percentage <= 1
                    ret.append(
                        {
                            "target": framework,
                            "name": f'{test_result["name"]} ({endpoint_mode})',
                            "stddev": test_result[benchmark_mode]["stddev"] if is_valid else 0,
                            "score_mean": test_result[benchmark_mode]["mean"] if is_valid else 0,
                            "score_50": test_result[benchmark_mode]["percentiles"]["50"] if is_valid else 0,
                            "score_75": test_result[benchmark_mode]["percentiles"]["75"] if is_valid else 0,
                            "score_90": test_result[benchmark_mode]["percentiles"]["90"] if is_valid else 0,
                            "score_95": test_result[benchmark_mode]["percentiles"]["95"] if is_valid else 0,
                            "score_99": test_result[benchmark_mode]["percentiles"]["99"] if is_valid else 0,
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
    percentile: str,
    output_dir: Path,
    benchmark_mode: BenchmarkMode,
    formats: tuple[str, ...],
    error_bars: bool,
    category: str | None = None,
):
    targets = df["target"].unique()
    benchmark_codes = sorted(df["name"].unique())

    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    plot = sns.barplot(
        data=df,
        x="name",
        y=f"score_{percentile}",
        hue="target",
        hue_order=targets,
        order=benchmark_codes,
        palette=COLOR_PALETTE,
        edgecolor="#FFFFFF",
        errorbar=None,
        width=0.7,
        ax=ax,
    )
    ax.set(xlabel="benchmark type", ylabel=None)
    plt.legend()

    mt_fmt = "mean" if percentile == "mean" else f"{percentile}th percentile"
    if benchmark_mode == "rps":
        title = f"Requests per second - {mt_fmt} (higher is better)"
        ax.yaxis.set_major_formatter(lambda i, pos: str(int(i / 1000)) + "k")
    else:
        title = f"Latency - {mt_fmt} (lower is better)"
        ax.yaxis.set_major_formatter(lambda i, pos: f"{i / 1000}ms")

    plot.set(title=title)

    plt.xticks(rotation=60, horizontalalignment="right")
    plt.tight_layout()

    if error_bars:
        x_coords = [p.get_x() + 0.5 * p.get_width() for p in ax.patches]
        y_coords = [p.get_height() for p in ax.patches]
        plt.errorbar(x=x_coords, y=y_coords, yerr=df["stddev"], fmt="none", c="k", capsize=4)

    plt.xticks(rotation=60, horizontalalignment="right")
    plt.tight_layout()

    for format in formats:
        filename = f"{benchmark_mode}_{percentile}.{format}"
        if category:
            filename = f"{category}_{filename}"
        plt.savefig(output_dir / filename)
        plt.close()


def _draw_percentile_plots(
    *,
    df: pd.DataFrame,
    percentiles: tuple[str, ...],
    output_dir: Path,
    benchmark_mode: BenchmarkMode,
    formats: tuple[str, ...],
    error_bars: bool,
    category: str | None = None,
):
    for percentile in percentiles:
        _draw_plot(
            df=df,
            percentile=percentile,
            output_dir=output_dir,
            benchmark_mode=benchmark_mode,
            formats=formats,
            error_bars=error_bars,
            category=category,
        )


def make_plots(
    *,
    percentiles: tuple[str, ...],
    error_bars: bool,
    run_number: int | None,
    formats: tuple[str, ...] = ("png",),
    split_categories: bool,
) -> None:
    cwd = Path.cwd()
    run_number, results = collect_results(run_number)
    output_dir = cwd / "plots" / f"run_{run_number}"
    output_dir.mkdir(exist_ok=True, parents=True)

    benchmark_modes: tuple[BenchmarkMode, ...] = ("rps", "latency")

    for benchmark_mode in benchmark_modes:
        if not all(benchmark_mode in mode_results for mode_results in results.values()):
            continue
        if split_categories:
            for category in ENDPOINT_CATEGORIES:
                df = _data_for_plot(results, benchmark_mode, category)
                if df is None:
                    continue
                _draw_percentile_plots(
                    df=df,
                    percentiles=percentiles,
                    output_dir=output_dir,
                    benchmark_mode=benchmark_mode,
                    formats=formats,
                    error_bars=error_bars,
                    category=category,
                )
        else:
            df = _data_for_plot(results, benchmark_mode, ENDPOINT_CATEGORIES)
            if df is None:
                continue
            _draw_percentile_plots(
                df=df,
                percentiles=percentiles,
                output_dir=output_dir,
                benchmark_mode=benchmark_mode,
                formats=formats,
                error_bars=error_bars,
            )
