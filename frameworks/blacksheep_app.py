import urllib.parse
from typing import TYPE_CHECKING

import anyio
from blacksheep import Application, Request, Response, json, text, Cookie
from blacksheep.server.responses import file, no_content
from blacksheep.testing import TestClient

from . import data

if TYPE_CHECKING:
    from .test import EndpointSpec


RESPONSE_COOKIES = [Cookie(name=name, value=value) for name, value in data.RESPONSE_COOKIES.items()]

app = Application()


# json


@app.router.get("/async-plaintext-6k")
async def async_plaintext_6k() -> Response:
    return text(data.TEXT_6k)


@app.router.get("/sync-plaintext-6k")
def sync_plaintext_6k() -> Response:
    return text(data.TEXT_6k)


@app.router.get("/async-plaintext-70k")
async def async_plaintext_70k() -> Response:
    return text(data.TEXT_70k)


@app.router.get("/sync-plaintext-70k")
def sync_plaintext_70k() -> Response:
    return text(data.TEXT_70k)


# JSON response


@app.router.get("/async-json-2k")
async def async_json_2k() -> Response:
    return json(data.JSON_2K)


@app.router.get("/sync-json-2k")
def sync_json_2k() -> Response:
    return json(data.JSON_2K)


@app.router.get("/async-json-10k")
async def async_json_10k() -> Response:
    return json(data.JSON_10K)


@app.router.get("/sync-json-10k")
def sync_json_10k() -> Response:
    return json(data.JSON_10K)


@app.router.get("/async-json-450k")
async def async_json_450k() -> Response:
    return json(data.JSON_450K)


@app.router.get("/sync-json-450k")
def sync_json_450k() -> Response:
    return json(data.JSON_450K)


# params


@app.router.get("/async-no-params")
async def async_no_params() -> Response:
    return no_content()


@app.router.get("/sync-no-params")
def sync_no_params() -> Response:
    return no_content()


@app.router.get("/async-path-params/{first}")
async def async_path_params(first: int) -> Response:
    return no_content()


@app.router.get("/sync-path-params/{first}")
def sync_path_params(first: int) -> Response:
    return no_content()


@app.router.get("/async-query-param")
async def async_query_params(request: Request) -> Response:
    first = int(request.query.get("first")[0])
    return no_content()


@app.router.get("/sync-query-param")
def sync_query_params(request: Request) -> Response:
    first = int(request.query.get("first")[0])
    return no_content()


@app.router.get("/async-mixed-params/{second}")
async def async_mixed_params(request: Request, second: int) -> Response:
    first = int(request.query.get("first")[0])
    return no_content()


@app.router.get("/sync-mixed-params/{second}")
def sync_mixed_params(request: Request, second: int) -> Response:
    first = int(request.query.get("first")[0])
    return no_content()


# headers


@app.router.get("/async-request-headers")
async def async_request_headers(request: Request) -> Response:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.get_tuples(b"header_1")
    return no_content()


@app.router.get("/sync-request-headers")
def sync_request_headers(request: Request) -> Response:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.get_tuples(b"header_1")
    return no_content()


@app.router.get("/async-response-headers")
async def async_response_headers() -> Response:
    res = no_content()
    res.headers.update({k.encode("latin-1"): v.encode("latin-1") for k, v in data.RESPONSE_HEADERS.items()})
    return res


@app.router.get("/sync-response-headers")
def sync_response_headers() -> Response:
    res = no_content()
    res.headers.update({k.encode("latin-1"): v.encode("latin-1") for k, v in data.RESPONSE_HEADERS.items()})
    return res


# cookies


@app.router.get("/async-request-cookies")
async def async_request_cookies(request: Request) -> Response:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value
    return no_content()


@app.router.get("/sync-request-cookies")
def sync_request_cookies(request: Request) -> Response:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value
    return no_content()


@app.router.get("/async-response-cookies")
async def async_response_cookies() -> Response:
    res = no_content()
    res.set_cookies(RESPONSE_COOKIES)
    return res


@app.router.get("/sync-response-cookies")
def sync_response_cookies() -> Response:
    res = no_content()
    res.set_cookies(RESPONSE_COOKIES)
    return res


# url


@app.router.get("/async-url-access")
async def async_url_access(request: Request) -> None:
    url = urllib.parse.urlsplit(request._url)
    scheme = request.url.schema
    netloc = url.netloc
    path = request.url.path
    fragment = request.url.fragment
    query = request.url.query
    username = url.username
    password = url.password
    port = request.url.port
    hostname = url.hostname
    for param, value in request.url.query.items():
        pass


@app.router.get("/sync-url-access")
def sync_url_access(request: Request) -> None:
    url = urllib.parse.urlsplit(request._url)
    scheme = request.url.schema
    netloc = url.netloc
    path = request.url.path
    fragment = request.url.fragment
    query = request.url.query
    username = url.username
    password = url.password
    port = request.url.port
    hostname = url.hostname
    for param, value in request.url.query.items():
        pass


# files


@app.router.get("/async-file-response-100B")
async def async_file_response_100b() -> Response:
    content = await anyio.Path(data.RESPONSE_FILE_100B).read_bytes()
    return file(content, file_name="response_file", content_type="application/x-binary")


@app.router.get("/async-file-response-50K")
async def async_file_response_50k() -> Response:
    content = await anyio.Path(data.RESPONSE_FILE_50K).read_bytes()
    return file(content, file_name="response_file", content_type="application/x-binary")


@app.router.get("/async-file-response-1K")
async def async_file_response_1k() -> Response:
    content = await anyio.Path(data.RESPONSE_FILE_1K).read_bytes()
    return file(content, file_name="response_file", content_type="application/x-binary")


@app.router.get("/async-file-response-1M")
async def async_file_response_1m() -> Response:
    content = await anyio.Path(data.RESPONSE_FILE_1M).read_bytes()
    return file(content, file_name="response_file", content_type="application/x-binary")


@app.router.get("/sync-file-response-100B")
def sync_file_response_100b() -> Response:
    return file(data.RESPONSE_FILE_100B.read_bytes(), file_name="response_file", content_type="application/x-binary")


@app.router.get("/sync-file-response-50K")
def sync_file_response_50k() -> Response:
    return file(data.RESPONSE_FILE_50K.read_bytes(), file_name="response_file", content_type="application/x-binary")


@app.router.get("/sync-file-response-1K")
def sync_file_response_1k() -> Response:
    return file(data.RESPONSE_FILE_1K.read_bytes(), file_name="response_file", content_type="application/x-binary")


@app.router.get("/sync-file-response-1M")
def sync_file_response_1m() -> Response:
    return file(data.RESPONSE_FILE_1M.read_bytes(), file_name="response_file", content_type="application/x-binary")


def run_spec_test(url: str, spec: "EndpointSpec") -> None:
    async def inner() -> None:
        await app.start()
        client = TestClient(app=app)
        res = await client.get(
            url,
            headers=spec["request"].get("headers", {}),
            query=spec["request"].get("params", {}),
            cookies=spec["request"].get("cookies", {}),
        )
        assert res.status == spec["result"]["status_code"]
        if expect_bytes := spec["result"].get("bytes"):
            content = await res.content.read()
            assert expect_bytes == content
        if expect_text := spec["result"].get("text"):
            assert expect_text == await res.text()
        if expect_json := spec["result"].get("json"):
            assert expect_json == await res.json()

    anyio.run(inner)
