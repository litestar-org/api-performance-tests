from collections import defaultdict
from pathlib import Path

from .types import (
    BenchmarkMode,
    EndpointCategory,
    EndpointDict,
    EndpointMode,
    FrameworkSpec,
    TestSpec,
)

ENDPOINTS: dict[EndpointCategory, dict[str, EndpointDict]] = {
    "plaintext": {
        "plaintext-100B": {"name": "plaintext 100 bytes"},
        "plaintext-1K": {"name": "plaintext 1kB"},
        "plaintext-10K": {"name": "plaintext 10kB"},
        "plaintext-100K": {"name": "plaintext 100kB"},
        "plaintext-500K": {"name": "plaintext 500kB"},
        "plaintext-1M": {"name": "plaintext 1MB"},
        "plaintext-5M": {"name": "plaintext 5MB"},
    },
    "json": {
        "json-1K": {"name": "json 1kB"},
        "json-10K": {"name": "json 10kB"},
        "json-100K": {"name": "json 100kB"},
        "json-500K": {"name": "json 500kB"},
        "json-1M": {"name": "json 1MB"},
        "json-5M": {"name": "json 5MB"},
    },
    "files": {
        "file-response-100B": {"name": "file response 100 bytes"},
        "file-response-1K": {"name": "file response 1kB"},
        "file-response-10K": {"name": "file response 10kB"},
        "file-response-100K": {"name": "file response 100kB"},
        "file-response-500K": {"name": "file response 500kB"},
        "file-response-1M": {"name": "file response 1MB"},
        "file-response-5M": {"name": "file response 5MB"},
    },
    "params": {
        "no-params": {"name": "no params"},
        "path-params/42": {"name": "path params"},
        "query-param?first=42": {"name": "query params"},
        "mixed-params/42?first=21": {"name": "mixed params"},
    },
    "dynamic-response": {
        "response-headers": {"name": "response headers"},
        "response-cookies": {"name": "response cookies"},
    },
}

ENDPOINT_CATEGORIES: tuple[EndpointCategory, ...] = tuple(ENDPOINTS.keys())


def make_spec(
    *,
    frameworks: tuple[str, ...],
    endpoint_modes: tuple[EndpointMode, ...] | EndpointMode,
    categories: tuple[EndpointCategory, ...] | EndpointCategory,
    warmup_time: int | None = None,
    time_limit: int | None = None,
    request_limit: int | None = None,
    rate_limit: int | None = None,
    benchmark_modes: tuple[BenchmarkMode, ...] | BenchmarkMode,
) -> list[FrameworkSpec]:
    if isinstance(endpoint_modes, str):
        endpoint_modes = (endpoint_modes,)
    if isinstance(categories, str):
        categories = (categories,)
    if isinstance(benchmark_modes, str):
        benchmark_modes = (benchmark_modes,)

    test_specs = [
        TestSpec(
            path=f"/{endpoint_mode}-{path}",
            endpoint_mode=endpoint_mode,
            benchmark_mode=benchmark_mode,
            category=category,
            name=args["name"],
            headers=args.get("headers") or [],
            warmup_time=warmup_time,
            time_limit=time_limit if benchmark_mode == "rps" else None,
            request_limit=request_limit if benchmark_mode == "latency" else None,
            rate_limit=rate_limit if benchmark_mode == "latency" else None,
            slug_name=f"{endpoint_mode}-{path.split('?')[0]}",
        )
        for benchmark_mode in benchmark_modes
        for endpoint_mode in endpoint_modes
        for category in categories
        for path, args in ENDPOINTS[category].items()
    ]

    framework_specs = []
    requested_frameworks = defaultdict(list)
    for framework in frameworks:
        name, *parts = framework.split("@", 1)
        version = parts[0] if parts else None
        requested_frameworks[name].append(version)

    for path in (Path.cwd() / "frameworks").iterdir():
        if path.is_file() and path.name.endswith("_app.py"):
            name = path.name.removesuffix("_app.py")
            if name not in requested_frameworks:
                continue
            for requested_version in requested_frameworks.get(name, []):
                framework_specs.append(
                    FrameworkSpec(
                        name=name,
                        version=requested_version,
                        path=path,
                        tests=test_specs,
                    )
                )

    return framework_specs
