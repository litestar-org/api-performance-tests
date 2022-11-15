import json
from pathlib import Path
from typing import Generator, NamedTuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

root_path = Path()
results_dir = root_path / "results"


class Percentiles(NamedTuple):
    p_50: int
    p_75: int
    p_90: int
    p_95: int
    p_99: int


class ResultStats(NamedTuple):
    mean: int
    max: int
    std_dev: int


class TestResult(NamedTuple):
    name: str
    benchmark_code: str
    test_type: str
    is_async: bool
    url: str
    method: str
    req_1xx: int
    req_2xx: int
    req_3xx: int
    req_4xx: int
    req_5xx: int
    latency: ResultStats
    rps: ResultStats
    rps_percentiles: Percentiles


def collect_results() -> Generator[TestResult, None, None]:
    for file in results_dir.glob("*.json"):
        target, sync_async, test_type, *_ = file.name.split("-")
        raw_test_data = json.loads(file.read_text())
        is_async = sync_async == "async"
        url = raw_test_data["spec"]["url"]

        benchmark_code = "/a-" if is_async else "/s-"
        if "/128" in url:
            benchmark_code += "pp"
        elif "query-param" in url:
            benchmark_code += "qp"
        elif "mixed-params" in url:
            benchmark_code += "mp"
        else:
            benchmark_code += "np"

        yield TestResult(
            name=target,
            benchmark_code=benchmark_code,
            is_async=is_async,
            test_type=test_type,
            url=url,
            method=raw_test_data["spec"]["method"],
            req_1xx=raw_test_data["result"]["req1xx"],
            req_2xx=raw_test_data["result"]["req2xx"],
            req_3xx=raw_test_data["result"]["req3xx"],
            req_4xx=raw_test_data["result"]["req4xx"],
            req_5xx=raw_test_data["result"]["req5xx"],
            latency=ResultStats(
                mean=raw_test_data["result"]["latency"]["mean"],
                max=raw_test_data["result"]["latency"]["max"],
                std_dev=raw_test_data["result"]["latency"]["stddev"],
            ),
            rps=ResultStats(
                mean=raw_test_data["result"]["rps"]["mean"],
                max=raw_test_data["result"]["rps"]["max"],
                std_dev=raw_test_data["result"]["rps"]["stddev"],
            ),
            rps_percentiles=Percentiles(
                p_50=raw_test_data["result"]["rps"]["percentiles"]["50"],
                p_75=raw_test_data["result"]["rps"]["percentiles"]["75"],
                p_90=raw_test_data["result"]["rps"]["percentiles"]["90"],
                p_95=raw_test_data["result"]["rps"]["percentiles"]["95"],
                p_99=raw_test_data["result"]["rps"]["percentiles"]["99"],
            ),
        )


def build_df(results: Generator[TestResult, None, None]) -> pd.DataFrame:
    data = [
        {
            "branch": result.name,
            "sync_async": result.is_async,
            "test_type": result.test_type,
            "url": result.url,
            "benchmark_code": result.benchmark_code,
            "benchmark_result": result.rps_percentiles.p_95,
            "benchmark_result_mean": result.rps.mean,
            "stddev": result.rps.std_dev,
        }
        for result in results
    ]
    data = sorted(data, key=lambda r: r["branch"])
    df = pd.DataFrame(data)
    return df


def draw_plot(df: pd.DataFrame) -> None:
    _df_test_data = df[df["test_type"] == "plaintext"]
    branches = df["branch"].unique()
    benchmark_codes = sorted(df["benchmark_code"].unique())

    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    sns.barplot(
        data=_df_test_data,
        x="benchmark_code",
        y="benchmark_result",
        hue="branch",
        hue_order=branches,
        order=benchmark_codes,
        palette=[
            "#30323D",
            "#5C80BC",
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
    ).set(
        title="Requests Processed - (higher is better)",
    )
    ax.yaxis.set_major_formatter(lambda i, pos: str(int(i / 1000)) + "k")

    x_coords = [p.get_x() + 0.5 * p.get_width() for p in ax.patches]
    y_coords = [p.get_height() for p in ax.patches]
    plt.errorbar(x=x_coords, y=y_coords, yerr=df["stddev"], fmt="none", c="k", capsize=4)

    fig.savefig(results_dir / "result.png")


def main() -> None:
    results = collect_results()
    df = build_df(results)
    draw_plot(df)


if __name__ == "__main__":
    main()
