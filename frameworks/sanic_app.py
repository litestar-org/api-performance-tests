import urllib.parse
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import anyio
from sanic import HTTPResponse, Request, Sanic
from sanic.application.constants import Mode
from sanic.application.motd import MOTD
from sanic.log import LOGGING_CONFIG_DEFAULTS
from sanic.response import ResponseStream, empty, file, file_stream, json, text

import test_data

if TYPE_CHECKING:
    from test_frameworks import EndpointSpec


log_config = {
    **LOGGING_CONFIG_DEFAULTS,
    "version": 1,
    "disable_existing_loggers": True,
    "loggers": {
        "sanic.root": {"level": "ERROR", "handlers": ["null"]},
        "sanic.error": {
            "level": "DEBUG",
            "handlers": ["error_console", "null"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "DEBUG",
            "handlers": ["null"],
            "propagate": True,
            "qualname": "sanic.access",
        },
        "app": {"level": "ERROR", "handlers": ["null"], "propagate": True, "qualname": "app"},
    },
    "handlers": {
        "null": {"class": "logging.NullHandler", "formatter": "generic"},
        "console": {"class": "logging.NullHandler", "formatter": "generic"},
        "error_console": {"class": "logging.NullHandler", "formatter": "generic"},
        "access_console": {"class": "logging.NullHandler", "formatter": "access"},
        "app_console": {"class": "logging.NullHandler", "formatter": "generic"},
    },
}
app = Sanic("MyApp", log_config=log_config)
app.config.ACCESS_LOG = False

MOTD.output = MagicMock()

# json


@app.route("/async-plaintext-6k")
async def async_plaintext_6k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_6k)


@app.route("/sync-plaintext-6k")
def sync_plaintext_6k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_6k)


@app.route("/async-plaintext-70k")
async def async_plaintext_70k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_70k)


@app.route("/sync-plaintext-70k")
def sync_plaintext_70k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_70k)


# JSON response


@app.route("/async-json-2k")
async def async_json_2k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_2K)


@app.route("/sync-json-2k")
def sync_json_2k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_2K)


@app.route("/async-json-10k")
async def async_json_10k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_10K)


@app.route("/sync-json-10k")
def sync_json_10k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_10K)


@app.route("/async-json-450k")
async def async_json_450k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_450K)


@app.route("/sync-json-450k")
def sync_json_450k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_450K)


# params


@app.route("/async-no-params")
async def async_no_params(request: Request) -> HTTPResponse:
    return empty()


@app.route("/sync-no-params")
def sync_no_params(request: Request) -> HTTPResponse:
    return empty()


@app.route("/async-path-params/<first:int>")
async def async_path_params(request: Request, first: int) -> HTTPResponse:
    return empty()


@app.route("/sync-path-params/<first:int>")
def sync_path_params(request: Request, first: int) -> HTTPResponse:
    return empty()


@app.route("/async-query-param")
async def async_query_params(request: Request) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


@app.route("/sync-query-param")
def sync_query_params(request: Request) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


@app.route("/async-mixed-params/<second:int>")
async def async_mixed_params(request: Request, second: int) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


@app.route("/sync-mixed-params/<second:int>")
def sync_mixed_params(request: Request, second: int) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


# headers


@app.route("/async-request-headers")
async def async_request_headers(request: Request) -> HTTPResponse:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.getall("header_1")
    return empty()


@app.route("/sync-request-headers")
def sync_request_headers(request: Request) -> HTTPResponse:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.getall("header_1")
    return empty()


@app.route("/async-response-headers")
async def async_response_headers(request: Request) -> HTTPResponse:
    return empty(headers=test_data.RESPONSE_HEADERS)


@app.route("/sync-response-headers")
def sync_response_headers(request: Request) -> HTTPResponse:
    return empty(headers=test_data.RESPONSE_HEADERS)


# cookies


@app.route("/async-request-cookies")
async def async_request_cookies(request: Request) -> HTTPResponse:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value
    return empty()


@app.route("/sync-request-cookies")
def sync_request_cookies(request: Request) -> HTTPResponse:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value
    return empty()


@app.route("/async-response-cookies")
async def async_response_cookies(request: Request) -> HTTPResponse:
    res = empty()
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.cookies[key] = value
    return res


@app.route("/sync-response-cookies")
def sync_response_cookies(request: Request) -> HTTPResponse:
    res = empty()
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.cookies[key] = value
    return res


# url


@app.route("/async-url-access")
async def async_url_access(request: Request) -> None:
    url = urllib.parse.urlsplit(request.url)
    scheme = url.scheme  # noqa: F841
    netloc = url.netloc  # noqa: F841
    path = url.path  # noqa: F841
    fragment = url.fragment  # noqa: F841
    query = url.query  # noqa: F841
    username = url.username  # noqa: F841
    password = url.password  # noqa: F841
    port = url.port  # noqa: F841
    hostname = url.hostname  # noqa: F841
    for param, value in request.args.items():  # noqa: B007
        pass


@app.route("/sync-url-access")
def sync_url_access(request: Request) -> None:
    url = urllib.parse.urlsplit(request.url)
    scheme = url.scheme  # noqa: F841
    netloc = url.netloc  # noqa: F841
    path = url.path  # noqa: F841
    fragment = url.fragment  # noqa: F841
    query = url.query  # noqa: F841
    username = url.username  # noqa: F841
    password = url.password  # noqa: F841
    port = url.port  # noqa: F841
    hostname = url.hostname  # noqa: F841
    for param, value in request.args.items():  # noqa: B007
        pass


# files


@app.route("/async-file-response-100B")
async def async_file_response_100b(request: Request) -> HTTPResponse:
    return await file(location=test_data.RESPONSE_FILE_100B, filename="response_file")


@app.route("/async-file-response-50K")
async def async_file_response_50k(request: Request) -> HTTPResponse:
    return await file(location=test_data.RESPONSE_FILE_50K, filename="response_file")


@app.route("/async-file-response-1K")
async def async_file_response_1k(request: Request) -> HTTPResponse:
    return await file(location=test_data.RESPONSE_FILE_1K, filename="response_file")


@app.route("/async-file-response-1M")
async def async_file_response_1m(request: Request) -> ResponseStream:
    return await file_stream(location=test_data.RESPONSE_FILE_1M, filename="response_file")


@app.route("/sync-file-response-100B")
def sync_file_response_100b(request: Request) -> HTTPResponse:
    with anyio.start_blocking_portal() as portal:
        return portal.call(file, test_data.RESPONSE_FILE_100B)


@app.route("/sync-file-response-50K")
def sync_file_response_50k(request: Request) -> HTTPResponse:
    with anyio.start_blocking_portal() as portal:
        return portal.call(file, test_data.RESPONSE_FILE_50K)


@app.route("/sync-file-response-1K")
def sync_file_response_1k(request: Request) -> HTTPResponse:
    with anyio.start_blocking_portal() as portal:
        return portal.call(file, test_data.RESPONSE_FILE_1K)


@app.route("/sync-file-response-1M")
def sync_file_response_1m(request: Request) -> HTTPResponse:
    with anyio.start_blocking_portal() as portal:
        return portal.call(file, test_data.RESPONSE_FILE_1M)


def run_spec_test(url: str, spec: "EndpointSpec") -> None:
    app.state.mode = Mode.PRODUCTION
    req, res = app.test_client.get(url, **spec.get("request", {}))
    assert res.status_code == spec["result"]["status_code"]
    if expect_bytes := spec["result"].get("bytes"):
        assert expect_bytes == res.content
    if expect_text := spec["result"].get("text"):
        assert expect_text == res.text
    if expect_json := spec["result"].get("json"):
        assert res.json == expect_json
