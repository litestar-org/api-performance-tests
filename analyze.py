import json
from collections.abc import Generator, Iterable
from pathlib import Path
from typing import Literal, TypedDict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

root_path = Path()

Percentile = Literal["50", "75", "90", "95", "99"]
Metric = Literal["rps", "latency"]

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

Percentiles = TypedDict("Percentiles", {"50": int, "75": int, "90": int, "95": int, "99": int})


class ResultStats(TypedDict):
    mean: int
    max: int
    stddev: int


class RPSResults(ResultStats):
    percentiles: Percentiles


class TestResult(TypedDict):
    target: str
    benchmark_code: str
    test_type: str
    is_async: bool
    url: str
    method: str
    latency: ResultStats
    rps: RPSResults


def collect_results(results_dir: Path) -> Generator[TestResult, None, None]:
    for target_dir in results_dir.iterdir():
        for file in target_dir.glob("*.json"):
            sync_async, test_type, *_ = file.name.split("-")
            raw_test_data = json.loads(file.read_text())
            is_async = sync_async == "async"
            url = raw_test_data["spec"]["url"]
            if raw_test_data["result"]["req4xx"] or raw_test_data["result"]["req5xx"]:
                print(f"Result set {file} contains error responses")  # noqa: T201

            if "/128" in url:
                benchmark_code = "path params"
            elif "query-param" in url:
                benchmark_code = "query params"
            elif "mixed-params" in url:
                benchmark_code = "mixed params"
            else:
                benchmark_code = "no params"
            benchmark_code += " (a)" if is_async else "( s)"

            yield TestResult(
                target=target_dir.name,
                benchmark_code=benchmark_code,
                is_async=is_async,
                test_type=test_type,
                url=url,
                **raw_test_data["result"],
            )


def build_df(results: Iterable[TestResult], percentile: Percentile) -> pd.DataFrame:
    data = [
        {
            "target": result["target"],
            "sync_async": result["is_async"],
            "test_type": result["test_type"],
            "url": result["url"],
            "benchmark_code": result["benchmark_code"],
            "benchmark_result": result["rps"]["percentiles"][percentile],
            "stddev": result["rps"]["stddev"],
        }
        for result in results
    ]
    data = sorted(data, key=lambda r: r["target"])
    df = pd.DataFrame(data)
    return df


def build_latency_df(results: Iterable[TestResult]) -> pd.DataFrame:
    data = [
        {
            "target": result["target"],
            "sync_async": result["is_async"],
            "test_type": result["test_type"],
            "url": result["url"],
            "benchmark_code": result["benchmark_code"],
            "benchmark_result": result["latency"]["mean"],
            "stddev": result["latency"]["stddev"],
        }
        for result in results
    ]
    data = sorted(data, key=lambda r: r["target"])
    df = pd.DataFrame(data)
    return df


def _configure_plot(df: pd.DataFrame, title: str, test_type: str = "plaintext") -> tuple:
    _df_test_data = df[df["test_type"] == test_type]
    targets = df["target"].unique()
    benchmark_codes = sorted(df["benchmark_code"].unique())

    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    plot = sns.barplot(
        data=_df_test_data,
        x="benchmark_code",
        y="benchmark_result",
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

    plot.set(title=title)

    plt.xticks(rotation=60, horizontalalignment="right")
    plt.tight_layout()
    return fig, ax


def draw_plot(
    df: pd.DataFrame,
    output_dir: Path,
    percentile: Percentile,
    test_type: str,
) -> None:
    fig, ax = _configure_plot(
        df,
        test_type=test_type,
        title=f"Requests per second - {percentile}th percentile  (higher is better)",
    )

    ax.yaxis.set_major_formatter(lambda i, pos: str(int(i / 1000)) + "k")

    x_coords = [p.get_x() + 0.5 * p.get_width() for p in ax.patches]
    y_coords = [p.get_height() for p in ax.patches]
    plt.errorbar(x=x_coords, y=y_coords, yerr=df["stddev"], fmt="none", c="k", capsize=4)
    plt.xticks(rotation=60, horizontalalignment="right")
    plt.tight_layout()

    fig.savefig(output_dir / f"{output_dir.stem}_rps_{percentile}.png")


def draw_latency_plot(df: pd.DataFrame, output_dir: Path, test_type: str) -> None:
    fig, ax = _configure_plot(df, test_type=test_type, title="Latency - (lower is better)")
    fig.savefig(output_dir / f"{output_dir.stem}_latency.png")


def make_rps_plot(percentile: Percentile | Literal["all"] = "95", test_type: str = "plaintext") -> None:
    results_dir = root_path / "results"
    results = list(collect_results(results_dir))
    percentiles: list[Percentile]
    if percentile == "all":
        percentiles = ["50", "75", "90", "95", "99"]
    else:
        percentiles = [percentile]
    for p in percentiles:
        df = build_df(results, percentile=p)
        draw_plot(df, results_dir, percentile=p, test_type=test_type)


def make_latency_plot(test_type: str = "plaintext") -> None:
    results_dir = root_path / "results"
    df = build_latency_df(collect_results(results_dir))
    draw_latency_plot(df, results_dir)
