import atexit
import json
import time
from pathlib import Path
from typing import Any

import docker
import httpx
from docker.models.containers import Container
from rich.console import Console

from .spec import make_spec
from .types import (
    BenchmarkMode,
    EndpointCategory,
    EndpointMode,
    FrameworkSpec,
    TestSpec,
)
from .util import get_error_percentage

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


class Runner:
    def __init__(
        self,
        *,
        frameworks: tuple[str, ...],
        endpoint_modes: tuple[EndpointMode, ...] | EndpointMode,
        categories: tuple[EndpointCategory, ...] | EndpointCategory,
        warmup_time: int | None = None,
        time_limit: int | None = None,
        request_limit: int | None = None,
        rate_limit: int | None = None,
        benchmark_modes: tuple[BenchmarkMode, ...] | BenchmarkMode,
    ) -> None:
        self.docker_client = docker.from_env()
        self.console = Console()
        self.root_path = Path.cwd()
        self.results_dir = self.root_path / "results"
        self.results_file = self._init_results_file()
        self._endpoint_modes = endpoint_modes
        self._benchmark_modes = benchmark_modes
        self._categories = categories
        self._request_limit = request_limit
        self._rate_limit = rate_limit
        self._time_limit = time_limit
        self._warmup_time = warmup_time

        self.specs = make_spec(
            frameworks=frameworks,
            endpoint_modes=endpoint_modes,
            categories=categories,
            request_limit=request_limit,
            rate_limit=rate_limit,
            time_limit=time_limit,
            benchmark_modes=benchmark_modes,
            warmup_time=warmup_time,
        )
        atexit.register(self._stop_all_containers)

    def print_suite_config(self) -> None:
        self.console.print(f"Benchmark modes: [magenta]{','.join(self._benchmark_modes)}")
        if "rps" in self._benchmark_modes:
            self.console.print(f"RPS benchmarks duration: {self._time_limit} seconds")
        if "latency" in self._benchmark_modes:
            self.console.print(f"Latency benchmarks RPS limit: {self._rate_limit}")
            self.console.print(f"Latency benchmarks requests limit: {self._request_limit}")
        self.console.print(f"Warmup time: [magenta]{self._warmup_time} seconds")
        self.console.print(f"Endpoint modes: [magenta]{', '.join(self._endpoint_modes)}")
        self.console.print(f"Endpoint categories: [magenta]{', '.join(self._categories)}")
        self.console.print(f"Frameworks: [magenta]{', '.join(f.version_name for f in self.specs)}")

    def _init_results_file(self) -> Path:
        self.results_dir.mkdir(exist_ok=True)
        numbers = [int(file.stem.split("_")[-1]) for file in self.results_dir.glob("run_*.json")]
        run_number = max(numbers) + 1 if numbers else 1
        return self.results_dir / f"run_{run_number}.json"

    def _write_results(self, target: str, spec: TestSpec, results: dict[str, Any]) -> None:
        if not self.results_file.exists():
            current_results = {}
        else:
            current_results = json.loads(self.results_file.read_text())
        current_results.setdefault(target, {})
        current_results[target].setdefault(spec.benchmark_mode, {})
        current_results[target][spec.benchmark_mode].setdefault(spec.endpoint_mode, {})
        current_results[target][spec.benchmark_mode][spec.endpoint_mode].setdefault(spec.category, [])
        current_results[target][spec.benchmark_mode][spec.endpoint_mode][spec.category].append(
            {"name": spec.name, **results["result"]}
        )
        self.results_file.write_text(json.dumps(current_results, indent=2))

    def _run_image(self, image: str) -> Container:
        for container in self.docker_client.containers.list(ignore_removed=True):
            if image in container.image.tags:
                container.stop()

        return self.docker_client.containers.run(image=image, ports={SERVER_PORT: SERVER_PORT}, detach=True)

    def _run_bench_in_container(self, *args: str) -> str:
        container = self.docker_client.containers.run(
            "starlite-api-bench:runner", "./bombardier " + " ".join(args), network_mode="host", detach=True
        )
        container.wait()
        return container.logs().decode()

    def _stop_all_containers(self) -> None:
        with self.console.status("[yellow]Stopping running containers"):
            for container in self.docker_client.containers.list(ignore_removed=True):
                if any(tag.startswith("starlite-api-bench:") for tag in container.image.tags):
                    container.stop()

    def run_benchmark(self, test_spec: TestSpec) -> dict[str, Any]:
        with self.console.status("  [yellow]Warming up endpoint"):
            self._run_bench_in_container(
                f"http://127.0.0.1:{SERVER_PORT}{test_spec.path}",
                "--no-print",
                *_header_args_from_spec(test_spec),
                f"--rate=10",
                f"--duration={test_spec.warmup}s",
            )
            time.sleep(2)

        with self.console.status(f"  [cyan]Running: {test_spec.pretty_name}"):
            res = self._run_bench_in_container(
                f"http://127.0.0.1:{SERVER_PORT}{test_spec.path}",
                "--latencies",
                "--format=json",
                "--print=result",
                *_args_from_spec(test_spec),
            )
        results = json.loads(res)
        error_percentage = get_error_percentage(results["result"])
        if error_percentage:
            self.console.print(f"    [red]Completed {test_spec.pretty_name} with errors ({error_percentage}%)")
        else:
            self.console.print(f"    [green]Completed: {test_spec.pretty_name}")
        return results

    def run_benchmarks(self, framework_spec: FrameworkSpec) -> None:

        with self.console.status(f"[yellow]Starting container: {framework_spec.image_tag}"):
            container = self._run_image(framework_spec.image_tag)
        self.console.print("  [cyan]Container started")

        with self.console.status("[yellow]Waiting for server to come online"):
            _wait_for_online()
        self.console.print("  [cyan]Server online")
        self.console.print("  [blue]Running benchmarks")

        for test_spec in framework_spec.tests:
            results = self.run_benchmark(test_spec)
            self._write_results(
                target=framework_spec.version_name,
                spec=test_spec,
                results=results,
            )

        with self.console.status("  [yellow]Stopping container"):
            container.stop()
        self.console.print("  [blue]Container stopped")

    def run(self) -> None:
        self._stop_all_containers()

        for framework_spec in self.specs:
            self.console.print(f"[blue]Suite: {framework_spec.version_name}")
            self.run_benchmarks(framework_spec=framework_spec)
