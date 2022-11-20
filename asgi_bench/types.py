from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict
from urllib.parse import urlparse

EndpointMode = Literal["sync", "async"]
EndpointCategory = Literal["plaintext", "json", "params", "dynamic-response", "files"]
BenchmarkMode = Literal["rps", "latency"]


@dataclass
class TestSpec:
    category: EndpointCategory
    name: str
    slug_name: str
    path: str
    headers: list[tuple[str, str]]
    endpoint_mode: EndpointMode
    benchmark_mode: BenchmarkMode
    time_limit: int | None = None
    request_limit: int | None = None
    rate_limit: int | None = None
    warmup: int = 5

    @property
    def pretty_name(self) -> str:
        return f"{self.benchmark_mode} - {self.name} ({self.endpoint_mode})"


class EndpointDict(TypedDict, total=False):
    headers: list[tuple[str, str]] | None
    name: str


FRAMEWORK_REPOS = {
    "starlite": "https://github.com/starlite-api/starlite.git",
    "starlette": "https://github.com/encode/starlette.git",
    "fastapi": "https://github.com/tiangolo/fastapi.git",
    "sanic": "https://github.com/sanic-org/sanic.git",
    "blacksheep": "https://github.com/Neoteroi/BlackSheep.git",
}


@dataclass
class FrameworkSpec:
    name: str
    path: Path
    tests: list[TestSpec]
    version: str | None = None

    @property
    def image_tag(self) -> str:
        versioned_name = self.version_name.replace(":", "_").replace("/", "_").replace(".git", "")
        return f"starlite-api-bench:{versioned_name}"

    @property
    def version_name(self) -> str:
        if not self.version:
            return self.name
        if self.is_git_target:
            git_target = self.version.removeprefix("git+")
            if git_target.startswith("https"):
                target = urlparse(git_target).path
            elif git_target.startswith("ssh"):
                target = git_target.split(":", 1)[-1]
            else:
                target = git_target
        else:
            target = self.version
        return f"{self.name}:{target}"

    @property
    def pip_package(self) -> str:
        if not self.version:
            return self.name
        if self.is_git_target:
            if self.version.removeprefix("git+").startswith(("https", "ssh")):
                return self.version
            git_target = self.version.split("git+", 1)[-1]
            return f"git+{FRAMEWORK_REPOS[self.name]}@{git_target}"
        return f"{self.name}=={self.version}"

    @property
    def is_git_target(self) -> bool:
        return bool(self.version and self.version.startswith("git+"))

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
