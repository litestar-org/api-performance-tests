from typing import TYPE_CHECKING

from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.testclient import TestClient
from starlette.status import HTTP_204_NO_CONTENT

import test_data

if TYPE_CHECKING:
    from test_frameworks import EndpointSpec

app = FastAPI()


# plaintext response


@app.get("/async-plaintext-6k", response_class=PlainTextResponse)
async def async_plaintext_6k() -> str:
    return test_data.TEXT_6k


@app.get("/sync-plaintext-6k", response_class=PlainTextResponse)
def sync_plaintext_6k() -> str:
    return test_data.TEXT_6k


@app.get("/async-plaintext-70k", response_class=PlainTextResponse)
async def async_plaintext_70k() -> str:
    return test_data.TEXT_70k


@app.get("/sync-plaintext-70k", response_class=PlainTextResponse)
def sync_plaintext_70k() -> str:
    return test_data.TEXT_70k


# JSON response


@app.get("/async-json-2k")
async def async_json_2k() -> dict[str, str]:
    return test_data.JSON_2K


@app.get("/sync-json-2k")
def sync_json_2k() -> dict[str, str]:
    return test_data.JSON_2K


@app.get("/async-json-10k")
async def async_json_10k() -> dict[str, str]:
    return test_data.JSON_10K


@app.get("/sync-json-10k")
def sync_json_10k() -> dict[str, str]:
    return test_data.JSON_10K


@app.get("/async-json-450k")
async def async_json_450k() -> dict[str, str]:
    return test_data.JSON_450K


@app.get("/sync-json-450k")
def sync_json_450k() -> dict[str, str]:
    return test_data.JSON_450K


# params


@app.get("/async-no-params", status_code=HTTP_204_NO_CONTENT)
async def async_no_params() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/sync-no-params", status_code=HTTP_204_NO_CONTENT)
def sync_no_params() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/async-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT)
async def async_path_params(first: int) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/sync-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT)
def sync_path_params(first: int) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/async-query-param", status_code=HTTP_204_NO_CONTENT)
async def async_query_params(first: int) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/sync-query-param", status_code=HTTP_204_NO_CONTENT)
def sync_query_params(first: int) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/async-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT)
async def async_mixed_params(first: int, second: int) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/sync-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT)
def sync_mixed_params(first: int, second: int) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


# headers


@app.get("/async-request-headers")
async def async_request_headers(request: Request) -> Response:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.getlist("header_1")
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/sync-request-headers")
def sync_request_headers(request: Request) -> Response:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.getlist("header_1")
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/async-response-headers")
async def async_response_headers() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


@app.get("/sync-response-headers")
def sync_response_headers() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


# cookies


@app.get("/async-request-cookies")
async def async_request_cookies(request: Request) -> Response:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/sync-request-cookies")
def sync_request_cookies(request: Request) -> Response:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.get("/async-response-cookies")
async def async_response_cookies() -> Response:
    res = Response(status_code=HTTP_204_NO_CONTENT)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


@app.get("/sync-response-cookies")
def sync_response_cookies() -> Response:
    res = Response(status_code=HTTP_204_NO_CONTENT)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


# url


@app.route("/async-url-access")
async def async_url_access(request: Request) -> None:
    scheme = request.url.scheme  # noqa: F841
    netloc = request.url.netloc  # noqa: F841
    path = request.url.path  # noqa: F841
    fragment = request.url.fragment  # noqa: F841
    query = request.url.query  # noqa: F841
    username = request.url.username  # noqa: F841
    password = request.url.password  # noqa: F841
    port = request.url.port  # noqa: F841
    hostname = request.url.hostname  # noqa: F841
    for param, value in request.query_params.items():  # noqa: B007
        pass


@app.route("/sync-url-access")
def sync_url_access(request: Request) -> None:
    scheme = request.url.scheme  # noqa: F841
    netloc = request.url.netloc  # noqa: F841
    path = request.url.path  # noqa: F841
    fragment = request.url.fragment  # noqa: F841
    query = request.url.query  # noqa: F841
    username = request.url.username  # noqa: F841
    password = request.url.password  # noqa: F841
    port = request.url.port  # noqa: F841
    hostname = request.url.hostname  # noqa: F841
    for param, value in request.query_params.items():  # noqa: B007
        pass


# files


@app.get("/async-file-response-100B")
async def async_file_response_100b() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_100B, filename="response_file")


@app.get("/async-file-response-50K")
async def async_file_response_50k() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_50K, filename="response_file")


@app.get("/async-file-response-1K")
async def async_file_response_1k() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_1K, filename="response_file")


@app.get("/async-file-response-1M")
async def async_file_response_1m() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_1M, filename="response_file")


@app.get("/sync-file-response-100B")
def sync_file_response_100b() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_100B, filename="response_file")


@app.get("/sync-file-response-50K")
def sync_file_response_50k() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_50K, filename="response_file")


@app.get("/sync-file-response-1K")
def sync_file_response_1k() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_1K, filename="response_file")


@app.get("/sync-file-response-1M")
def sync_file_response_1m() -> FileResponse:
    return FileResponse(path=test_data.RESPONSE_FILE_1M, filename="response_file")


def run_spec_test(url: str, spec: "EndpointSpec") -> None:
    with TestClient(app=app) as client:
        res = client.get(url, **spec.get("request", {}))
        assert res.status_code == spec["result"]["status_code"]
        if expect_bytes := spec["result"].get("bytes"):
            assert expect_bytes == res.content
        if expect_text := spec["result"].get("text"):
            assert expect_text == res.text
        if expect_json := spec["result"].get("json"):
            assert res.json() == expect_json
