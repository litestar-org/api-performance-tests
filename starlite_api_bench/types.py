from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict
from urllib.parse import urlparse

EndpointMode = Literal["sync", "async"]
EndpointCategory = Literal["plaintext", "json", "params", "headers", "cookies", "url", "files"]
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
        return f"{self.name} ({self.endpoint_mode})"


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
