import json
from pathlib import Path
from typing import Generator, Iterable, Literal, TypedDict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

root_path = Path()

Percentile = Literal["50", "75", "90", "95", "99"]
Metric = Literal["rps", "latency"]

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
    for file in results_dir.glob("*.json"):
        sync_async, test_type, *_ = file.name.split("-")
        raw_test_data = json.loads(file.read_text())
        is_async = sync_async == "async"
        url = raw_test_data["spec"]["url"]

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
            target=file.parent.name,
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
            "benchmark_result_mean": result["rps"]["mean"],
            "benchmark_result": result["rps"]["percentiles"][percentile],
            "stddev": result["rps"]["stddev"],
        }
        for result in results
    ]
    data = sorted(data, key=lambda r: r["target"])
    df = pd.DataFrame(data)
    return df


def draw_plot(
    df: pd.DataFrame,
    output_dir: Path,
    percentile: Percentile,
    metric: Metric,
) -> None:
    _df_test_data = df[df["test_type"] == "plaintext"]
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
        palette=[
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
        ],
        edgecolor="#FFFFFF",
        errorbar=None,
        width=0.7,
        ax=ax,
    )
    ax.set(xlabel="benchmark type", ylabel=None)
    plt.legend()

    if metric == "load":
        ax.yaxis.set_major_formatter(lambda i, pos: str(int(i / 1000)) + "k")
        plot.set(
            title=f"Requests per second - {percentile}th percentile  (higher is better)",
        )
    else:
        plot.set(title=f"Latency - {percentile}th percentile (lower is better)")

    x_coords = [p.get_x() + 0.5 * p.get_width() for p in ax.patches]
    y_coords = [p.get_height() for p in ax.patches]
    plt.errorbar(x=x_coords, y=y_coords, yerr=df["stddev"], fmt="none", c="k", capsize=4)
    plt.xticks(rotation=60, horizontalalignment="right")
    plt.tight_layout()

    fig.savefig(output_dir.parent / f"result_{output_dir.stem}_{percentile}.png")


def make_plot(percentile: Percentile | Literal["all"] = "95") -> None:
    results_dir = root_path / "results"
    for dir_ in results_dir.iterdir():
        if dir_.is_dir():
            results = list(collect_results(dir_))
            percentiles: list[Percentile]
            if percentile == "all":
                percentiles = ["50", "75", "90", "95", "99"]
            else:
                percentiles = [percentile]
            for p in percentiles:
                df = build_df(results, percentile=p)
                draw_plot(df, dir_, percentile=p, metric="load")


if __name__ == "__main__":
    make_plot()
