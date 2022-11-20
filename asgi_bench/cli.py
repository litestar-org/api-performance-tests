import click

from asgi_bench import results
from asgi_bench.build import build_docker_images
from asgi_bench.runner import Runner
from asgi_bench.spec import ENDPOINT_CATEGORIES
from asgi_bench.types import BenchmarkMode, EndpointCategory, EndpointMode


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("frameworks", nargs=-1)
@click.option("--rebuild", is_flag=True, show_default=True, help="rebuild git-based images")
@click.option("-w", "--warmup_time", default=5, show_default=True)
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
    warmup: int,
    rps: bool,
    latency: bool,
    limit: int,
    requests: int,
    duration: int,
    endpoint_mode: tuple[EndpointMode, ...],
    endpoint_category: tuple[EndpointCategory, ...],
) -> None:
    benchmark_modes: tuple[BenchmarkMode, ...] = ()
    if rps:
        benchmark_modes = ("rps",)
    if latency:
        benchmark_modes = (*benchmark_modes, "latency")

    runner = Runner(
        frameworks=frameworks,
        endpoint_modes=endpoint_mode,
        categories=endpoint_category,
        request_limit=requests,
        rate_limit=limit,
        time_limit=duration,
        benchmark_modes=benchmark_modes,
        warmup_time=warmup,
    )

    runner.print_suite_config()

    build_docker_images(framework_specs=runner.specs, rebuild_git=rebuild)

    runner.run()


@cli.command("results")
@click.option("-r", "--run", "run_name", type=int, help="run to analyze (defaults to latest run)")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["png", "svg", "html"]),
    default=("png",),
    show_default=True,
    multiple=True,
    help="format to save plots as",
)
@click.option(
    "-p",
    "--percentile",
    type=click.Choice(["mean", "50", "75", "90", "95", "99"]),
    default=("mean", "50", "75", "90", "95", "99"),
    multiple=True,
)
@click.option(
    "-E",
    "--no-error-bars",
    default=False,
    is_flag=True,
    help="include error bars",
    show_default=True,
)
@click.option("-s", "--split-categories", is_flag=True, help="split categories into separate files")
def results_command(
    run_name: int | None,
    format: tuple[str, ...],
    percentile: tuple[str, ...],
    no_error_bars: bool,
    split_categories: bool,
) -> None:
    results.make_plots(
        formats=format,
        percentiles=percentile,
        run_number=run_name,
        error_bars=not no_error_bars,
        split_categories=split_categories,
    )
