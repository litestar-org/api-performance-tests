from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from secrets import token_hex

import docker  # type: ignore
from rich.console import Console

from .types import FrameworkSpec

console = Console()


@contextmanager
def temporary_dockerfile(framework_spec: FrameworkSpec) -> Generator[Path, None, None]:
    # because the docker sdk does not allow to pass a context while also supplying a
    # file-like object, we have to store it on disk temporarily

    template = (Path.cwd() / "DockerfileFrameworks.tpl").read_text()
    content = template.format(
        pip_package=framework_spec.pip_package,
        framework=framework_spec.name,
    )
    dockerfile = Path.cwd() / ".dockerfile.tmp"
    dockerfile.write_text(content)
    yield dockerfile
    dockerfile.unlink()


def build_docker_images(framework_specs: list[FrameworkSpec], rebuild_git: bool = False) -> None:
    console.print("[cyan]Building images")
    client = docker.from_env()

    with console.status("[yellow]Building runner image"):
        client.images.build(path=".", dockerfile="DockerfileBench", tag="starlite-api-bench:runner")
    console.print("[green]  Runner image built successfully")

    for framework in framework_specs:
        pretty_name = f"{framework.version_name} ({framework.image_tag})"
        status = console.status(f"[yellow]Building image for {pretty_name}")
        status.start()
        build_args = {}
        if rebuild_git and framework.is_git_target:
            # if it's a git target, we inject a random string into the "pip install"-stage
            # to ensure it will be rebuilt
            build_args["RANDOM_STRING"] = token_hex()
        with temporary_dockerfile(framework) as dockerfile:
            client.images.build(
                path=".",
                dockerfile=dockerfile,
                tag=framework.image_tag,
                buildargs=build_args,
                rm=True,
                quiet=False,
            )
        status.stop()
        console.print(f"  [green]Image for {pretty_name} built successfully")

    console.print(f"  [green]{len(framework_specs)} images built successfully")
