from pathlib import Path

import pytest

from asgi_bench.types import FrameworkSpec


@pytest.mark.parametrize(
    "type_,version,clean_version,version_name,pip_package,image_tag",
    [
        ("pip", "v1.0.0", "v1.0.0", "v1.0.0", "litestar==v1.0.0", "litestar_v1.0.0"),
        (
            "git",
            "git+v1.0.0",
            "v1.0.0",
            "v1.0.0",
            "git+https://github.com/litestar-org/litestar.git@v1.0.0",
            "litestar_v1.0.0",
        ),
        (
            "file",
            "file+./my_package/src",
            "./my_package/src",
            "local",
            "./my_package/src",
            "litestar_local",
        ),
        ("docker", "docker+my_image", "my_image", "my_image", None, "litestar_my_image"),
    ],
)
def test_spec_targets(
    type_: str,
    version: str,
    pip_package: str | None,
    clean_version: str,
    image_tag: str,
    version_name: str,
):
    spec = FrameworkSpec(name="litestar", version=version, path=Path(), tests=[])
    if pip_package:
        assert spec.pip_package == pip_package
    assert spec.typed_version == (type_, clean_version)
    assert spec.image_tag == f"litestar-bench:{image_tag}"
    assert spec.version_name == f"litestar:{version_name}"
