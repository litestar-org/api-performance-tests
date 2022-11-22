import multiprocessing
from contextlib import contextmanager
from typing import TypedDict

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
            # "access_log": False,
            # "log_level": 50,
        },
        daemon=True,
    )
    proc.start()
    try:
        yield
    finally:
        proc.kill()


class ResultSpec(TypedDict):
    status_code: int
    bytes: bytes | None
    json: dict | None
    text: str | None


class RequestSpec(TypedDict, total=False):
    headers: dict[str, str]
    params: dict[str, str]
    cookies: dict[str, str]


class EndpointSpec(TypedDict):
    result: ResultSpec
    request: RequestSpec


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
}


@pytest.mark.parametrize("framework", ["starlite", "starlette", "fastapi", "sanic", "blacksheep"])
@pytest.mark.parametrize("path_spec", list(ENDPOINT_SPEC.items()))
@pytest.mark.parametrize("endpoint_type", ["sync", "async"])
def test_framework(framework: str, path_spec: tuple[str, EndpointSpec], endpoint_type: str) -> None:
    framework = getattr(frameworks, f"{framework}_app")
    path, spec = path_spec

    with run_app(framework.app):
        url = f"http://127.0.0.1:8181/{endpoint_type}-{path}"
        res = httpx.get(url, **spec.get("request", {}))

        assert res.status_code == spec["result"]["status_code"]
        if expect_bytes := spec["result"].get("bytes"):
            assert expect_bytes == res.content
        if expect_text := spec["result"].get("text"):
            assert expect_text == res.text
        if expect_json := spec["result"].get("json"):
            assert res.json() == expect_json
