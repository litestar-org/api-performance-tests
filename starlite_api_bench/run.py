import atexit
import json
import time
from pathlib import Path
from typing import Any

import docker
import httpx
from docker.models.containers import Container
from rich.console import Console

from .types import FrameworkSpec, TestSpec

console = Console()


SERVER_PORT = 8081


def _header_args_from_spec(test_spec: TestSpec) -> list[str]:
    params = []
    for header, value in test_spec.headers:
        params.append(f'--header="{header}: {value}"')
    return params


def _args_from_spec(test_spec: TestSpec) -> list[str]:
    args = [*_header_args_from_spec(test_spec)]
    if rate_limit := test_spec.rate_limit:
        args.append(f"--rate={rate_limit}")
    if request_limit := test_spec.request_limit:
        args.append(f"--requests={request_limit}")
    if duration := test_spec.time_limit:
        args.append(f"--duration={duration}s")
    return args


def _wait_for_online() -> bool:
    for _ in range(5):
        try:
            res = httpx.get(f"http://127.0.0.1:{SERVER_PORT}/sync-no-params", timeout=1)
            if res.status_code == 200:
                return True
        except httpx.HTTPError:
            time.sleep(1)
    return False


def run_image(image: str) -> Container:
    client = docker.from_env()
    for container in client.containers.list(ignore_removed=True):
        if image in container.image.tags:
            container.stop()

    return client.containers.run(image=image, ports={SERVER_PORT: SERVER_PORT}, detach=True)


def _run_bench_in_container(client: docker.DockerClient, *args) -> str:
    container = client.containers.run(
        "starlite-api-bench:runner", "./bombardier " + " ".join(args), network_mode="host", detach=True
    )
    container.wait()
    return container.logs().decode()


def _stop_all_containers() -> None:
    client = docker.from_env()
    with console.status("[yellow]Stopping running containers"):
        for container in client.containers.list(ignore_removed=True):
            if any(tag.startswith("starlite-api-bench:") for tag in container.image.tags):
                container.stop()


def run_benchmark(test_spec: TestSpec) -> dict[str, Any]:
    client = docker.from_env()
    with console.status("  [yellow]Warming up endpoint"):
        _run_bench_in_container(
            client,
            f"http://127.0.0.1:{SERVER_PORT}{test_spec.path}",
            f"--duration={test_spec.warmup}s",
            "--no-print",
            *_header_args_from_spec(test_spec),
        )

    with console.status(f"  [cyan]Running: {test_spec.pretty_name}"):
        res = _run_bench_in_container(
            client,
            f"http://127.0.0.1:{SERVER_PORT}{test_spec.path}",
            "--latencies",
            "--format=json",
            "--print=result",
            # *_args_from_spec(test_spec),
            "--duration=1s",
        )
        console.print(f"    [green]Completed: {test_spec.pretty_name}")
        return json.loads(res)


def _append_results_to_file(target: str, spec: TestSpec, results: dict[str, Any], results_file: Path) -> None:
    if not results_file.exists():
        current_results = {}
    else:
        current_results = json.loads(results_file.read_text())
    current_results.setdefault(target, {})
    current_results[target].setdefault(spec.benchmark_mode, {})
    current_results[target][spec.benchmark_mode].setdefault(spec.endpoint_mode, {})
    current_results[target][spec.benchmark_mode][spec.endpoint_mode].setdefault(spec.category, [])
    current_results[target][spec.benchmark_mode][spec.endpoint_mode][spec.category].append(
        {"name": spec.name, **results}
    )
    results_file.write_text(json.dumps(current_results, indent=2))


def _init_results_file(results_dir: Path) -> Path:
    results_dir.mkdir(exist_ok=True)
    numbers = [int(file.stem.split("_")[-1]) for file in results_dir.glob("run_*.json")]
    run_number = max(numbers) + 1 if numbers else 1
    return results_dir / f"run_{run_number}.json"


def run_benchmarks(*, framework_spec: FrameworkSpec, results_dir: Path) -> None:
    results_file = _init_results_file(results_dir)

    with console.status(f"[yellow]Starting container: {framework_spec.image_tag}"):
        container = run_image(framework_spec.image_tag)
    console.print("  [cyan]Container started")

    with console.status("[yellow]Waiting for server to come online"):
        _wait_for_online()
    console.print("  [cyan]Server online")
    console.print("  [blue]Running benchmarks")

    for test_spec in framework_spec.tests:
        results = run_benchmark(test_spec)
        _append_results_to_file(
            target=framework_spec.version_name,
            spec=test_spec,
            results=results,
            results_file=results_file,
        )

    with console.status("  [yellow]Stopping container"):
        container.stop()
    console.print("  [blue]Container stopped")


def run_benchmarks_on_targets(targets: list[FrameworkSpec], results_dir: Path) -> None:
    atexit.register(_stop_all_containers)
    _stop_all_containers()

    for framework_spec in targets:
        console.print(f"[blue]Suite: {framework_spec.version_name}")
        run_benchmarks(framework_spec=framework_spec, results_dir=results_dir)
