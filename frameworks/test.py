from typing import TypedDict

from starlite.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT

from . import data


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


ENDPOINT_SPEC: dict[str, EndpointSpec] = {
    # plaintext
    "plaintext-6k": {"result": {"status_code": HTTP_200_OK, "text": data.TEXT_6k}, "request": {}},
    "plaintext-70k": {"result": {"status_code": HTTP_200_OK, "text": data.TEXT_70k}, "request": {}},
    # json
    "json-2k": {"result": {"status_code": HTTP_200_OK, "json": data.JSON_2K}, "request": {}},
    "json-10k": {"result": {"status_code": HTTP_200_OK, "json": data.JSON_10K}, "request": {}},
    "json-450k": {"result": {"status_code": HTTP_200_OK, "json": data.JSON_450K}, "request": {}},
    # files
    "file-response-100B": {
        "result": {"status_code": HTTP_200_OK, "bytes": data.RESPONSE_FILE_100B.read_bytes()},
        "request": {},
    },
    "file-response-1K": {
        "result": {"status_code": HTTP_200_OK, "bytes": data.RESPONSE_FILE_1K.read_bytes()},
        "request": {},
    },
    "file-response-50K": {
        "result": {"status_code": HTTP_200_OK, "bytes": data.RESPONSE_FILE_50K.read_bytes()},
        "request": {},
    },
    "file-response-1M": {
        "result": {"status_code": HTTP_200_OK, "bytes": data.RESPONSE_FILE_1M.read_bytes()},
        "request": {},
    },
    # params
    "no-params": {"result": {"status_code": HTTP_204_NO_CONTENT, "content": None}, "request": {}},
    "path-params/42": {"result": {"status_code": HTTP_204_NO_CONTENT, "content": None}, "request": {}},
    "query-param": {
        "result": {"status_code": HTTP_204_NO_CONTENT, "content": None},
        "request": {"params": {"first": "42"}},
    },
    "mixed-params/11": {
        "result": {"status_code": HTTP_204_NO_CONTENT, "content": None},
        "request": {"params": {"first": "42"}},
    },
    # headers
    "request-headers": {
        "result": {"status_code": HTTP_204_NO_CONTENT, "content": None},
        "request": {"headers": data.RESPONSE_HEADERS},
    },
    "response-headers": {"result": {"status_code": HTTP_204_NO_CONTENT, "content": None}, "request": {}},
    # cookies
    "request-cookies": {
        "result": {"status_code": HTTP_204_NO_CONTENT, "content": None},
        "request": {"cookies": data.RESPONSE_COOKIES},
    },
    "response-cookies": {"result": {"status_code": HTTP_204_NO_CONTENT, "content": None}, "request": {}},
}


def test_all_frameworks() -> None:
    from frameworks import (
        blacksheep_app,
        fastapi_app,
        sanic_app,
        starlette_app,
        starlite_app,
    )

    for framework in [starlite_app, starlette_app, fastapi_app, sanic_app, blacksheep_app]:
        for endpoint_type in ["sync", "async"]:
            for path, spec in ENDPOINT_SPEC.items():
                url = f"/{endpoint_type}-{path}"
                try:
                    framework.run_spec_test(url, spec)
                except AssertionError:
                    print(f"Validation error for: {framework.__name__!r} - {url!r}")  # noqa: T201
