from pathlib import Path

import docker
from rich.console import Console

from .types import FrameworkSpec


class Context:
    def __init__(self, framework_specs: list[FrameworkSpec]) -> None:
        self.framework_specs = framework_specs
        self.docker_client = docker.from_env()
        self.console = Console()
        self.root_path = Path.cwd()
        self.results_dir = self.root_path / "results"
