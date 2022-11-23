from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict, TypeGuard
from urllib.parse import urlparse

EndpointMode = Literal["sync", "async"]
EndpointCategory = Literal["plaintext", "json", "params", "dynamic-response", "files", "dependency-injection"]
BenchmarkMode = Literal["rps", "latency"]
VersionPrefix = Literal["pip", "git", "docker", "file"]
Framework = Literal["starlite", "starlette", "fastapi", "sanic", "blacksheep"]

FRAMEWORK_REPOS = {
    "starlite": "https://github.com/starlite-api/starlite.git",
    "starlette": "https://github.com/encode/starlette.git",
    "fastapi": "https://github.com/tiangolo/fastapi.git",
    "sanic": "https://github.com/sanic-org/sanic.git",
    "blacksheep": "https://github.com/Neoteroi/BlackSheep.git",
}


@dataclass
class TestSpec:
    category: EndpointCategory
    name: str
    slug_name: str
    path: str
    headers: list[tuple[str, str]]
    endpoint_mode: EndpointMode
    benchmark_mode: BenchmarkMode
    is_supported: bool
    warmup_time: int | None = None
    time_limit: int | None = None
    request_limit: int | None = None
    rate_limit: int | None = None

    @property
    def pretty_name(self) -> str:
        return f"{self.benchmark_mode} - {self.name} ({self.endpoint_mode})"


def _validate_prefix(prefix: str) -> TypeGuard[VersionPrefix]:
    return prefix in {"pip", "git", "docker", "file"}


@dataclass
class FrameworkSpec:
    name: str
    path: Path
    tests: list[TestSpec]
    version: str | None = None

    @property
    def typed_version(self) -> tuple[VersionPrefix, str]:
        prefix: VersionPrefix = "pip"
        version = ""
        if self.version:
            if "+" in self.version:
                prefix_, version = self.version.split("+", 1)
                if not _validate_prefix(prefix_):
                    raise ValueError(f"Invalid version type: {prefix_!r}")
                prefix = prefix_
            else:
                version = self.version
        return prefix, version

    @property
    def is_git_target(self) -> bool:
        return self.typed_version[0] == "git"

    @property
    def is_local_target(self) -> bool:
        return self.typed_version[0] == "file"

    @property
    def is_docker_target(self) -> bool:
        return self.typed_version[0] == "docker"

    @property
    def is_pip_target(self) -> bool:
        return self.typed_version[0] == "pip"

    @property
    def image_tag(self) -> str:
        versioned_name = self.version_name.replace(":", "_").replace("/", "_").replace(".git", "")
        return f"starlite-api-bench:{versioned_name}"

    @property
    def build_stage_image(self) -> str | None:
        if self.is_docker_target:
            return self.typed_version[1]
        return None

    @property
    def version_name(self) -> str:
        if not self.version:
            return self.name
        prefix, version = self.typed_version
        if prefix == "git":
            if version.startswith("https"):
                version = urlparse(version).path
            elif version.startswith("ssh"):
                version = version.split(":", 1)[-1]
        elif prefix == "file":
            version = "local"
        return f"{self.name}:{version}"

    @property
    def pip_package(self) -> str:
        if not self.version:
            return self.name
        prefix, version = self.typed_version
        if prefix == "git":
            if version.startswith(("https", "ssh")):
                return f"git+{version}"
            return f"git+{FRAMEWORK_REPOS[self.name]}@{version}"
        elif prefix == "file":
            return version
        return f"{self.name}=={self.version}"

    @property
    def extra_requirements(self) -> list[str]:
        path = self.path.parent / f"requirements-{self.name}.txt"
        if path.exists():
            return path.read_text().splitlines()
        return []

    @property
    def pip_install_targets(self) -> str:
        args = [self.pip_package, *self.extra_requirements]
        return " ".join(args)


TestResultPercentiles = TypedDict("TestResultPercentiles", {"50": int, "75": int, "90": int, "95": int, "99": int})


class TestResultStats(TypedDict):
    mean: int
    max: int
    stddev: int
    percentiles: TestResultPercentiles


class TestResult(TypedDict):
    name: str
    timeTakenSeconds: int
    req1xx: int
    req2xx: int
    req3xx: int
    req4xx: int
    req5xx: int
    others: int
    latency: TestResultStats
    rps: TestResultStats


CategoryResults = dict[EndpointCategory, list[TestResult]]

EndpointModeResults = TypedDict("EndpointModeResults", {"sync": CategoryResults, "async": CategoryResults})


class SuiteResults(TypedDict):
    rps: EndpointModeResults
    latency: EndpointModeResults
