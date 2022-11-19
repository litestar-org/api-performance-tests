import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict

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
BenchmarkMode = Literal["rps", "latency"]


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
        bench_config.append(f"--duration={config.duration}s")
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
            with console.status(f"  [cyan]{config.mode.title()} benchmark running: {endpoint!r}"), open(
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
            console.print(f"  [green]{config.mode.title()} benchmark completed: {endpoint!r}")


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
    console.print(f"Mode:                   {config.mode}")
    console.print(f"Endpoint types:         {', '.join(config.endpoint_types)}")
    console.print(f"Test types:             {', '.join(config.test_types)}")
    console.print(f"Warmup duration:        {config.warmup_duration}")
    if config.duration:
        console.print(f"Benchmark duration:     {config.duration}")
    if config.request_limit:
        console.print(f"Requests:               {config.request_limit}")
    if config.rate_limit:
        console.print(f"Rate limit:             {config.rate_limit}")


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


class BenchCtx(TypedDict):
    warmup: int
    endpoints: list[EndpointType]
    types: tuple[TestType, ...]


def _run_bench_from_cmd(
    ctx: click.Context,
    frameworks: bool,
    branches: bool,
    targets: tuple[str, ...],
    config: SuiteConfig,
) -> None:
    if frameworks == branches:
        console.print("[red]--framework and --branches are mutually exclusive")
        console.print(ctx.get_help())
        ctx.abort()

    if frameworks:
        if targets == ("all",):
            targets = FRAMEWORKS
        diff = set(targets) - set(FRAMEWORKS)
        if diff:
            console.print(f"[red]Unsupported frameworks: {', '.join(diff)}")
            ctx.abort()
        run_framework_benchmarks(targets, config)
    if branches:
        run_branch_benchmarks(targets, config)


@click.group()
def cli() -> None:
    pass


@cli.group()
@click.option("-w", "--warmup", default=5)
@click.option(
    "-e",
    "--endpoints",
    type=click.Choice(["sync", "async"], case_sensitive=False),
    multiple=True,
    default=("sync", "async"),
)
@click.option("-t", "--type", type=click.Choice(["plaintext", "json"]), default=("plaintext",), multiple=True)
@click.pass_context
def bench(
    ctx: click.Context,
    warmup: int,
    endpoints: list[EndpointType],
    type: tuple[TestType, ...],
) -> None:
    ctx.ensure_object(dict)
    ctx.obj["warmup"] = warmup
    ctx.obj["endpoints"] = endpoints
    ctx.obj["types"] = type


@bench.command("rps")
@click.option("-f", "--frameworks", is_flag=True, default=False)
@click.option("-b", "--branches", is_flag=True, default=False)
@click.option("-d", "--duration", default=15, show_default=True)
@click.argument("targets", nargs=-1)
@click.pass_context
def rps_command(
    ctx: click.Context,
    frameworks: bool,
    branches: bool,
    targets: tuple[str, ...],
    duration: int,
) -> None:
    ctx_data: BenchCtx = ctx.obj
    config = SuiteConfig(
        test_types=ctx_data["types"],
        endpoint_types=ctx_data["endpoints"],
        warmup_duration=ctx_data["warmup"],
        mode="rps",
        duration=duration,
    )
    _run_bench_from_cmd(ctx=ctx, frameworks=frameworks, branches=branches, targets=targets, config=config)


@bench.command("latency")
@click.option("-f", "--frameworks", is_flag=True, default=False)
@click.option("-b", "--branches", is_flag=True, default=False)
@click.option("-l", "--limit", default=20, help="max requests per second", show_default=True)
@click.option("-r", "--requests", default=1000, help="total number of requests", show_default=True)
@click.argument("targets", nargs=-1)
@click.pass_context
def latency_cmd(
    ctx: click.Context, frameworks: bool, branches: bool, targets: tuple[str, ...], limit: int, requests: int
) -> None:
    ctx_data: BenchCtx = ctx.obj
    config = SuiteConfig(
        test_types=ctx_data["types"],
        endpoint_types=ctx_data["endpoints"],
        warmup_duration=ctx_data["warmup"],
        mode="latency",
        rate_limit=limit,
        request_limit=requests,
    )
    _run_bench_from_cmd(ctx=ctx, frameworks=frameworks, branches=branches, targets=targets, config=config)


@cli.command("analyze")
@click.option("-p", "--percentile", type=click.Choice(["50", "75", "90", "95", "99", "all"]), default="95")
@click.option("-m", "--metric", default="rps", type=click.Choice(["rps", "latency"]))
@click.option("-t", "--type", type=click.Choice(["plaintext", "json"]), default="plaintext")
def analyze_command(percentile: analyze.Percentile | Literal["all"], metric: str, type: TestType) -> None:
    if metric == "rps":
        analyze.make_rps_plot(percentile, test_type=type)
    else:
        analyze.make_latency_plot(test_type=type)


if __name__ == "__main__":
    cli()
