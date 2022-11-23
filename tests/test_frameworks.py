import multiprocessing
import time
from contextlib import contextmanager

import httpx
import pytest
import uvicorn

import frameworks
import test_data


@contextmanager
def run_app(app):
    proc = multiprocessing.Process(
        target=uvicorn.run,
        kwargs={
            "app": app,
            "port": "8181",
            "access_log": False,
            "log_level": 50,
        },
        daemon=True,
    )
    proc.start()
    time.sleep(2)
    try:
        yield
    finally:
        proc.kill()


ENDPOINT_SPEC = {
    **{
        f"plaintext-{size}": {
            "result": {"status_code": 200, "text": getattr(test_data, f"TEXT_{size}")},
            "request": {},
        }
        for size in ["100B", "1K", "10K", "100K", "500K", "1M", "5M"]
    },
    **{
        f"json-{size}": {
            "result": {"status_code": 200, "json": getattr(test_data, f"JSON_{size}")},
            "request": {},
        }
        for size in ["1K", "10K", "100K", "500K", "1M", "5M"]
    },
    **{
        f"file-response-{size}": {
            "result": {"status_code": 200, "bytes": getattr(test_data, f"FILE_{size}").read_bytes()},
            "request": {},
        }
        for size in ["1K", "10K", "100K", "500K", "1M", "5M"]
    },
    # params
    "no-params": {"result": {"status_code": 204, "content": None}, "request": {}},
    "path-params/42": {"result": {"status_code": 204, "content": None}, "request": {}},
    "query-param": {
        "result": {"status_code": 204, "content": None},
        "request": {"params": {"first": "42"}},
    },
    "mixed-params/11": {
        "result": {"status_code": 204, "content": None},
        "request": {"params": {"first": "42"}},
    },
    # headers
    "response-headers": {"result": {"status_code": 204, "content": None}, "request": {}},
    # cookies
    "response-cookies": {"result": {"status_code": 204, "content": None}, "request": {}},
    "dependencies-sync": {
        "result": {
            "status_code": 200,
            "json": ["sync_dependency_one", "sync_dependency_two", "sync_dependency_three"],
        },
        "request": {},
        "skip": ["starlette"],
    },
    "dependencies-async": {
        "result": {
            "status_code": 200,
            "json": ["async_dependency_one", "async_dependency_two", "async_dependency_three"],
        },
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep"],
    },
    "dependencies-mixed": {
        "result": {
            "status_code": 200,
            "json": [
                ["sync_dependency_one", "sync_dependency_two", "sync_dependency_three"],
                ["async_dependency_one", "async_dependency_two", "async_dependency_three"],
            ],
        },
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep"],
    },
}


@pytest.fixture(params=["starlite", "starlette", "fastapi", "sanic", "blacksheep"], scope="session")
def framework(request):
    framework_name = request.param
    module = getattr(frameworks, f"{framework_name}_app")
    with run_app(module.app):
        yield framework_name


@pytest.mark.parametrize("path", list(ENDPOINT_SPEC))
@pytest.mark.parametrize("endpoint_type", ["sync", "async"])
def test_framework(framework: str, path: str, endpoint_type: str) -> None:
    spec = ENDPOINT_SPEC[path]

    if framework in spec.get("skip", []):
        pytest.skip()

    url = f"http://127.0.0.1:8181/{endpoint_type}-{path}"
    res = httpx.get(url, **spec.get("request", {}))

    assert res.status_code == spec["result"]["status_code"]
    if expect_bytes := spec["result"].get("bytes"):
        assert expect_bytes == res.content
    if expect_text := spec["result"].get("text"):
        assert expect_text == res.text
    if expect_json := spec["result"].get("json"):
        # breakpoint()
        assert res.json() == expect_json
