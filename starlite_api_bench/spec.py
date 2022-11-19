from pathlib import Path
from typing import TypedDict

from .types import (
    BenchmarkMode,
    EndpointDict,
    EndpointMode,
    FrameworkSpec,
    TestCategory,
    TestSpec,
)

RESPONSE_HEADERS = {f"header_{i}": "value" for i in range(10)}
RESPONSE_COOKIES = {f"cookie_{i}": "value" for i in range(10)}


class Endpoints(TypedDict):
    plaintext: dict[str, EndpointDict]
    json: dict[str, EndpointDict]
    params: dict[str, EndpointDict]
    headers: dict[str, EndpointDict]
    cookies: dict[str, EndpointDict]
    url: dict[str, EndpointDict]
    files: dict[str, EndpointDict]


ENDPOINTS: Endpoints = {
    "plaintext": {
        "plaintext-6k": {"name": "plaintext 6kB"},
        "plaintext-70k": {"name": "plaintext 70kB"},
    },
    "json": {
        "json-2k": {"name": "JSON 2kB"},
        "json-10k": {"name": "JSON 10kB"},
        "json-450k": {"name": "JSON 450kB"},
    },
    "params": {
        "no-params": {"name": "no params"},
        "path-params/42": {"name": "path params"},
        "query-param?first=42": {"name": "query params"},
        "mixed-params/42?first=21": {"name": "mixed params"},
    },
    "headers": {
        "request-headers": {
            "name": "request headers",
            "headers": list(RESPONSE_HEADERS.items()),
        },
        "response-headers": {"name": "response headers"},
    },
    "cookies": {
        "request-cookies": {
            "name": "request cookies",
            "headers": [("Set-Cookie", f"{key}={value}") for key, value in RESPONSE_COOKIES.items()],
        },
        "response-cookies": {"name": "response cookies"},
    },
    "url": {
        "url-access": {"name": "url access"},
    },
    "files": {
        "file-response-100B": {"name": "file response 100 bytes"},
        "file-response-1K": {"name": "file response 1kB"},
        "file-response-50K": {"name": "file response 50kB"},
        "file-response-1M": {"name": "file response 1MB"},
    },
}

ENDPOINT_CATEGORIES = tuple(ENDPOINTS.keys())


def make_spec(
    *,
    frameworks: tuple[str, ...],
    endpoint_modes: tuple[EndpointMode, ...] | EndpointMode,
    categories: tuple[TestCategory, ...] | TestCategory,
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
    requested_frameworks = {}
    for framework in frameworks:
        name, *version = framework.split("@", 1)
        version = version[0] if version else None
        requested_frameworks[name] = version

    for path in (Path.cwd() / "frameworks").iterdir():
        if path.is_file() and path.name.endswith("_app.py"):
            name = path.name.removesuffix("_app.py")
            if name not in requested_frameworks:
                continue
            framework_specs.append(
                FrameworkSpec(
                    name=name,
                    version=requested_frameworks[name],
                    path=path,
                    tests=test_specs,
                )
            )

    return framework_specs
