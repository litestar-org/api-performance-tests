import shutil
import subprocess
import time
from pathlib import Path
from typing import Literal, NamedTuple
from dataclasses import dataclass

import click
import httpx
import rich

import analyze

ENDPOINTS = [
    "plaintext-mixed-params/256?first=128",
    "plaintext-no-params",
    "plaintext-query-param?first=128",
    "plaintext/128",
    "json-mixed-params/256?first=128",
    "json-no-params",
    "json-query-param?first=128",
    "json/128",
]

FRAMEWORKS = ["starlite", "starlette", "fastapi", "sanic", "blacksheep"]


SERVER_PORT = 8081
EndpointType = Literal["sync", "async"]
TestType = Literal["json", "plaintext"]
BenchmarkMode = Literal["load", "latency"]


@dataclass(frozen=True)
class SuiteConfig:
    warmup_duration: int
    endpoint_types: list[EndpointType]
    mode: BenchmarkMode
    test_types: tuple[TestType, ...]
    request_limit: int | None = None
    rate_limit: int | None = None
    duration: int | None = None


console = rich.console.Console()


def install_target_starlite(version: str) -> None:
    with console.status(f"  [yellow]Installing Starlite {version}"):
        proc = subprocess.run(
            ["pip", "install", f"git+https://github.com/starlite-api/starlite.git@{version}"],
            capture_output=True,
        )
    proc.check_returncode()
    console.print(f"  [green]Installed Starlite {version!r}")


def wait_for_online() -> bool:
    for _ in range(5):
        try:
            res = httpx.get(f"http://127.0.0.1:{SERVER_PORT}/sync-plaintext-no-params", timeout=1)
            if res.status_code == 200:
                return True
        except httpx.HTTPError:
            time.sleep(1)
    return False


def run_benchmarks(target: str, config: SuiteConfig) -> None:
    root_path = Path()
    results_path = root_path / "results" / target
    if results_path.exists():
        shutil.rmtree(results_path)
    results_path.mkdir(parents=True)

    bench_config = []
    if config.duration:
        bench_config.append(f"--duration={config.duration}")
    if config.rate_limit:
        bench_config.append(f"--rate={config.rate_limit}")
    if config.request_limit:
        bench_config.append(f"--requests={config.request_limit}")

    if not bench_config:
        raise ValueError("Invalid configuration")

    for endpoint_suffix in [e for e in ENDPOINTS if e.startswith(config.test_types)]:
        for endpoint_type in config.endpoint_types:
            endpoint = f"{endpoint_type}-{endpoint_suffix}"
            results_file = (results_path / endpoint.replace("/", "-")).with_suffix(".json")

            with console.status("  [yellow]Warming up endpoint"):
                subprocess.run(
                    [
                        "./bombardier",
                        f"http://127.0.0.1:{SERVER_PORT}/{endpoint}",
                        "--latencies",
                        f"--duration={config.warmup_duration}s",
                        "--no-print",
                    ]
                )
                time.sleep(1)
            with console.status(f"  [yellow]Running {config.mode} benchmark {endpoint!r}"), open(
                results_file, "w"
            ) as out:
                subprocess.run(
                    [
                        "./bombardier",
                        f"http://127.0.0.1:{SERVER_PORT}/{endpoint}",
                        *bench_config,
                        "--format=json",
                        "--print=result",
                    ],
                    stdout=out,
                )
            console.print(f"  [green]{config.mode} benchmark of {endpoint!r} complete")


def run_target(target: str, config: SuiteConfig, name: str = "") -> None:
    name = name or target
    root_path = Path()
    frameworks_path = root_path / "frameworks"
    app_file = frameworks_path / f"{target}_app.py"
    process = subprocess.Popen(
        [
            "uvicorn",
            "--no-access-log",
            "--loop",
            "uvloop",
            f"frameworks.{app_file.stem}:app",
            "--port",
            str(SERVER_PORT),
        ],
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    with console.status("  [yellow]Waiting for application server to come online"):
        if not wait_for_online():
            raise RuntimeError("server not available")
    console.print("  [green]Server online")
    run_benchmarks(name, config=config)

    console.print("  [yellow]Stopping server process")
    process.kill()


def _display_suite_config(config: SuiteConfig) -> None:
    console.print("[blue]Starting suite..")
    console.print(f"Mode: {config.mode}", justify="right")
    console.print(f"Endpoint types: {', '.join(config.endpoint_types)}", justify="right")
    console.print(f"Test types: {', '.join(config.test_types)}", justify="right")
    console.print(f"Warmup duration: {config.warmup_duration}", justify="right")
    if config.duration:
        console.print(f"Benchmark duration: {config.duration}", justify="right")
    if config.request_limit:
        console.print(f"Requests: {config.request_limit}", justify="right")
    if config.rate_limit:
        console.print(f"Rate limit: {config.rate_limit}", justify="right")


def _cleanup_results() -> None:
    root_path = Path()
    results_dir = root_path / "results"
    if not results_dir.exists():
        return
    for target in results_dir.iterdir():
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink(missing_ok=True)


def run_framework_benchmarks(frameworks: tuple[str, ...], config: SuiteConfig) -> None:
    _cleanup_results()
    _display_suite_config(config)
    for framework in frameworks:
        console.print(f"[blue]Selecting benchmark {framework!r}")
        run_target(framework, config=config)


def run_branch_benchmarks(branches: tuple[str, ...], config: SuiteConfig) -> None:
    _cleanup_results()
    _display_suite_config(config)
    for branch in branches:
        console.print(f"[blue]Selecting benchmark {branch!r}")
        install_target_starlite(branch)
        run_target("starlite", config=config, name=f"starlite_{branch.replace('.', '-')}")


@click.group()
def cli() -> None:
    pass


@cli.command("bench-frameworks")
@click.option("-f", "--frameworks", type=click.Choice([*FRAMEWORKS, "all"]), multiple=True)
@click.option("-d", "--duration", default=15)
@click.option("-w", "--warmup", default=5)
@click.option(
    "-e",
    "--endpoints",
    type=click.Choice(["sync", "async"], case_sensitive=False),
    multiple=True,
    default=("sync", "async"),
)
@click.option("-m", "--mode", type=click.Choice(["load", "latency"]), default="load")
@click.option("-t", "--type", type=click.Choice(["plaintext"]), default="plaintext", multiple=True)
def bench_frameworks(
    frameworks: tuple[str, ...],
    duration: int,
    warmup: int,
    endpoints: list[EndpointType],
    type: tuple[TestType, ...],
    mode: BenchmarkMode,
) -> None:
    if frameworks == ("all",):
        frameworks = FRAMEWORKS
    run_framework_benchmarks(
        frameworks,
        config=SuiteConfig(
            duration=duration,
            warmup_duration=warmup,
            endpoint_types=endpoints,
            mode=mode,
            test_types=type,
        ),
    )


@cli.command("bench-branches")
@click.argument("branches", nargs=-1)
@click.option("-d", "--duration", default=15)
@click.option("-w", "--warmup", default=5)
@click.option(
    "-e",
    "--endpoints",
    type=click.Choice(["sync", "async"], case_sensitive=False),
    multiple=True,
    default=("sync", "async"),
)
@click.option("-m", "--mode", type=click.Choice(["load", "latency"]), default="load")
@click.option("-t", "--type", type=click.Choice(["plaintext"]), default="plaintext", multiple=True)
def bench_branches(
    branches: tuple[str],
    duration: int,
    warmup: int,
    endpoints: list[EndpointType],
    mode: BenchmarkMode,
    type: tuple[TestType, ...],
) -> None:
    run_branch_benchmarks(
        branches,
        config=SuiteConfig(
            duration=duration,
            warmup_duration=warmup,
            endpoint_types=endpoints,
            mode=mode,
            test_types=type,
        ),
    )


@cli.command("analyze")
@click.option("-p", "--percentile", type=click.Choice(["50", "75", "90", "95", "99", "all"]), default="95")
@click.option("-m", "--metric", default="load", type=click.Choice(["load", "latency"]))
@click.option("-t", "--type", type=click.Choice(["plaintext", "json"]), default="plaintext")
def analyze_command(percentile: analyze.Percentile | Literal["all"], metric: str, type: TestType) -> None:
    if metric == "load":
        analyze.make_rps_plot(percentile, test_type=type)
    else:
        analyze.make_latency_plot(test_type=type)


if __name__ == "__main__":
    cli()
