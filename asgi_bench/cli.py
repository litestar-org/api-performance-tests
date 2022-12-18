import click

from asgi_bench import results
from asgi_bench.build import build_docker_images, remove_docker_images
from asgi_bench.runner import Runner
from asgi_bench.spec import ENDPOINT_CATEGORIES, FRAMEWORKS
from asgi_bench.types import BenchmarkMode, EndpointCategory, EndpointMode


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("frameworks", nargs=-1)
@click.option("--rebuild", is_flag=True, show_default=True, help="rebuild images")
@click.option("-w", "--warmup", default=5, show_default=True)
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
@click.option("-t", "--test", help="run a specific test", default=None)
@click.option("-v", "--validate-only", is_flag=True, default=False, help="only run endpoint validation")
def run(
    frameworks: tuple[str, ...],
    rebuild: bool,
    warmup: int,
    rps: bool,
    latency: bool,
    limit: int,
    requests: int,
    duration: int,
    validate_only: bool,
    endpoint_mode: tuple[EndpointMode, ...],
    endpoint_category: tuple[EndpointCategory, ...],
    test: str | None = None,
) -> None:
    if not frameworks:
        frameworks = FRAMEWORKS
    benchmark_modes: tuple[BenchmarkMode, ...] = ()
    if rps:
        benchmark_modes = ("rps",)
    if latency:
        benchmark_modes = (*benchmark_modes, "latency")

    if test and ":" in test:
        category, test = test.split(":")
        endpoint_category = (category,)  # type: ignore[assignment]

    runner = Runner(
        frameworks=frameworks,
        endpoint_modes=endpoint_mode,
        categories=endpoint_category,
        request_limit=requests,
        rate_limit=limit,
        time_limit=duration,
        benchmark_modes=benchmark_modes,
        warmup_time=warmup,
        test_name=test,
        validate_only=validate_only,
    )

    runner.print_suite_config()

    build_docker_images(framework_specs=runner.specs, rebuild=rebuild)

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
    type=click.Choice(["50", "75", "90", "95", "99"]),
    default=(),
    multiple=True,
)
@click.option("-s", "--split-percentiles", is_flag=True, help="split percentile results into separate files")
@click.option(
    "-t",
    "--tolerance",
    type=float,
    default=0.1,
    help="threshold of error responses at which a test will be considered invalid",
)
@click.option("-F", "--framework", multiple=True, default=None)
@click.option("-md", "--markdown", is_flag=True, help="output a markdown table")
@click.option("-h", "--html", is_flag=True, help="output an HTML page")
@click.option("-P", "--plots", is_flag=True, help="output plots")
def results_command(
    run_name: int | None,
    format: tuple[str, ...],
    percentile: tuple[str, ...],
    split_percentiles: bool,
    tolerance: float,
    framework: tuple[str, ...] | None,
    markdown: bool,
    html: bool,
    plots: bool,
) -> None:
    if plots:
        results.make_plots(
            formats=format,
            percentiles=percentile,
            run_number=run_name,
            split_percentiles=split_percentiles,
            tolerance=tolerance,
            frameworks=framework,
        )
    results.make_tables(run_number=run_name, frameworks=framework, markdown=markdown, html=html)


@cli.command(help="remove all benchmark docker images built")
@click.option("-f", "--force", is_flag=True)
def remove_images(force: bool):
    remove_docker_images(force=force)
