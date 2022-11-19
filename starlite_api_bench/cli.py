import click

from starlite_api_bench.build import build_docker_images
from starlite_api_bench.run import run_benchmarks_on_targets
from starlite_api_bench.spec import ENDPOINT_CATEGORIES, make_spec
from starlite_api_bench.types import BenchmarkMode, EndpointMode

from .context import Context


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("frameworks", nargs=-1)
@click.option("--rebuild", is_flag=True, show_default=True, help="rebuild git-based images")
@click.option("-R", "--rps", is_flag=True, help="run rps benchmarks")
@click.option("-L", "--latency", is_flag=True, help="run latency benchmarks")
@click.option("-l", "--limit", default=20, help="max requests per second for latency benchmarks", show_default=True)
@click.option(
    "-r", "--requests", default=1000, help="total number of requests for latency benchmarks", show_default=True
)
@click.option("-d", "--duration", default=15, show_default=True, help="duration of the rps benchmarks")
@click.option(
    "-e",
    "--endpoint-mode",
    type=click.Choice(["sync", "async"], case_sensitive=False),
    multiple=True,
    default=("sync", "async"),
    help="endpoint modes",
)
@click.option(
    "-c",
    "--endpoint-category",
    type=click.Choice(ENDPOINT_CATEGORIES, case_sensitive=False),
    default=ENDPOINT_CATEGORIES,
    multiple=True,
    show_default=True,
    help="endpoint category",
)
def run(
    frameworks: tuple[str, ...],
    rebuild: bool,
    rps: bool,
    latency: bool,
    limit: int,
    requests: int,
    duration: int,
    endpoint_mode: tuple[EndpointMode, ...],
    endpoint_category: tuple[str, ...],
) -> None:
    benchmark_modes: tuple[BenchmarkMode, ...] = ()
    if rps:
        benchmark_modes = ("rps",)
    if latency:
        benchmark_modes = (*benchmark_modes, "latency")
    specs = make_spec(
        frameworks=frameworks,
        endpoint_modes=endpoint_mode,
        categories="params",
        request_limit=requests,
        rate_limit=limit,
        time_limit=duration,
        benchmark_modes=benchmark_modes,
    )
    context = Context(framework_specs=specs)

    context.console.print(f"Benchmark modes: [magenta]{','.join(benchmark_modes)}")
    if "rps" in benchmark_modes:
        context.console.print(f"RPS benchmarks duration: {duration} seconds")
    if "latency" in benchmark_modes:
        context.console.print(f"Latency benchmarks RPS limit: {limit}")
        context.console.print(f"Latency benchmarks requests limit: {requests}")
    context.console.print(f"Endpoint modes: [magenta]{', '.join(endpoint_mode)}")
    context.console.print(f"Endpoint categories: [magenta]{', '.join(endpoint_category)}")
    context.console.print(f"Frameworks: [magenta]{', '.join(f.version_name for f in specs)}")

    build_docker_images(framework_specs=specs, rebuild_git=rebuild)
    run_benchmarks_on_targets(specs, context.results_dir)
