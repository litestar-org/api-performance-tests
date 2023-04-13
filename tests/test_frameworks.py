import multiprocessing
import time
from contextlib import contextmanager

import frameworks
import httpx
import pytest
import test_data
import uvicorn


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
            "skip-sync": ["sanic", "quart"],
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
        "skip": ["starlette", "quart"],
    },
    "dependencies-async": {
        "result": {
            "status_code": 200,
            "json": ["async_dependency_one", "async_dependency_two", "async_dependency_three"],
        },
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
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
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
    },
    "serialize-pydantic-50": {
        "result": {"status_code": 200, "json": test_data.PERSON_DATA_50},
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
    },
    "serialize-pydantic-100": {
        "result": {"status_code": 200, "json": test_data.PERSON_DATA_100},
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
    },
    "serialize-pydantic-500": {
        "result": {"status_code": 200, "json": test_data.PERSON_DATA_500},
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
    },
    "serialize-dataclasses-50": {
        "result": {"status_code": 200, "json": test_data.PERSON_DATA_50},
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
    },
    "serialize-dataclasses-100": {
        "result": {"status_code": 200, "json": test_data.PERSON_DATA_100},
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
    },
    "serialize-dataclasses-500": {
        "result": {"status_code": 200, "json": test_data.PERSON_DATA_500},
        "request": {},
        "skip": ["starlette", "sanic", "blacksheep", "quart"],
    },
    "post-json": {
        "result": {"status_code": 204},
        "request": {"json": test_data.JSON_1K, "method": "POST"},
        "skip-sync": ["starlette", "blacksheep", "quart"],
    },
    "post-multipart-form": {
        "result": {"status_code": 204},
        "request": {"content": test_data.MULTIPART_1K, "headers": test_data.MULTIPART_1K_HEADERS, "method": "POST"},
        "skip-sync": ["starlette", "fastapi", "blacksheep", "quart"],
    },
    "post-form-urlencoded": {
        "result": {"status_code": 204},
        "request": {
            "method": "POST",
            "content": test_data.FORM_URLENCODED_1K,
            "headers": test_data.FORM_URLENCODED_1K_HEADERS,
        },
        "skip-sync": ["starlette", "fastapi", "quart"],
    },
    "post-file": {
        "result": {"status_code": 204},
        "request": {
            "method": "POST",
            "files": {"test_file": test_data.FILE_1K.read_bytes()},
        },
        "skip-sync": ["starlette", "quart"],
    },
}


@pytest.fixture(
    params=[
        "litestar",
        "starlette",
        "fastapi",
        "sanic",
        "blacksheep",
        "quart",
    ],
    scope="session",
)
def framework(request):
    framework_name = request.param
    module = getattr(frameworks, f"{framework_name}_app")
    with run_app(module.app):
        yield framework_name


@pytest.mark.parametrize("path", list(ENDPOINT_SPEC))
@pytest.mark.parametrize("endpoint_type", ["sync", "async"])
def test_framework(framework: str, path: str, endpoint_type: str) -> None:
    spec = ENDPOINT_SPEC[path]

    skip = spec.get("skip", [])
    if endpoint_type == "async":
        skip.extend(spec.get("skip-async", []))
    else:
        skip.extend(spec.get("skip-sync", []))

    if framework in skip:
        pytest.skip()

    url = f"http://127.0.0.1:8181/{endpoint_type}-{path}"
    request = {"url": url, "method": "GET", **spec.get("request", {})}
    res = httpx.request(**request, timeout=10000)

    assert res.status_code == spec["result"]["status_code"]
    if expect_bytes := spec["result"].get("bytes"):
        assert expect_bytes == res.content
    if expect_text := spec["result"].get("text"):
        assert expect_text == res.text
    if expect_json := spec["result"].get("json"):
        assert res.json() == expect_json
