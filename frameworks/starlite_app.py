from starlite import Cookie, File, MediaType, Request, ResponseHeader, Starlite, TestClient, get
from starlite.status_codes import HTTP_204_NO_CONTENT

from . import data
from .test import EndpointSpec

response_headers = {name: ResponseHeader(value=value) for name, value in data.RESPONSE_HEADERS.items()}
response_cookies = [Cookie(key=key, value=value) for key, value in data.RESPONSE_COOKIES.items()]


# plaintext response


@get("/async-plaintext-6k", media_type=MediaType.TEXT)
async def async_plaintext_6k() -> str:
    return data.TEXT_6k


@get("/sync-plaintext-6k", media_type=MediaType.TEXT)
def sync_plaintext_6k() -> str:
    return data.TEXT_6k


@get("/async-plaintext-70k", media_type=MediaType.TEXT)
async def async_plaintext_70k() -> str:
    return data.TEXT_70k


@get("/sync-plaintext-70k", media_type=MediaType.TEXT)
def sync_plaintext_70k() -> str:
    return data.TEXT_70k


# JSON response


@get("/async-json-2k", media_type=MediaType.JSON)
async def async_json_2k() -> dict:
    return data.JSON_2K


@get("/sync-json-2k", media_type=MediaType.JSON)
def sync_json_2k() -> dict:
    return data.JSON_2K


@get("/async-json-10k", media_type=MediaType.JSON)
async def async_json_10k() -> dict:
    return data.JSON_10K


@get("/sync-json-10k", media_type=MediaType.JSON)
def sync_json_10k() -> dict:
    return data.JSON_10K


@get("/async-json-450k", media_type=MediaType.JSON)
async def async_json_450k() -> dict:
    return data.JSON_450K


@get("/sync-json-450k", media_type=MediaType.JSON)
def sync_json_450k() -> dict:
    return data.JSON_450K


# params


@get("/async-no-params", status_code=HTTP_204_NO_CONTENT)
async def async_no_params() -> None:
    pass


@get("/sync-no-params", status_code=HTTP_204_NO_CONTENT)
def sync_no_params() -> None:
    pass


@get("/async-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT)
async def async_path_params(first: int) -> None:
    pass


@get("/sync-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT)
def sync_path_params(first: int) -> None:
    pass


@get("/async-query-param", status_code=HTTP_204_NO_CONTENT)
async def async_query_params(first: int) -> None:
    pass


@get("/sync-query-param", status_code=HTTP_204_NO_CONTENT)
def sync_query_params(first: int) -> None:
    pass


@get("/async-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT)
async def async_mixed_params(first: int, second: int) -> None:
    pass


@get("/sync-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT)
def sync_mixed_params(first: int, second: int) -> None:
    pass


# headers


@get("/async-request-headers", status_code=HTTP_204_NO_CONTENT)
async def async_request_headers(request: Request) -> None:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.getall("header_1")


@get("/sync-request-headers", status_code=HTTP_204_NO_CONTENT)
def sync_request_headers(request: Request) -> None:
    header_dict = {}
    for header_name, header_value in request.headers.items():
        header_dict[header_name] = header_value
    request.headers.getall("header_1")


@get("/async-response-headers", response_headers=response_headers, status_code=HTTP_204_NO_CONTENT)
async def async_response_headers() -> None:
    pass


@get("/sync-response-headers", response_headers=response_headers, status_code=HTTP_204_NO_CONTENT)
def sync_response_headers() -> None:
    pass


# cookies


@get("/async-request-cookies", status_code=HTTP_204_NO_CONTENT)
async def async_request_cookies(request: Request) -> None:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value


@get("/sync-request-cookies", status_code=HTTP_204_NO_CONTENT)
def sync_request_cookies(request: Request) -> None:
    cookie_dict = {}
    for cookie_name, cookie_value in request.cookies.items():
        cookie_dict[cookie_name] = cookie_value


@get("/async-response-cookies", response_cookies=response_cookies, status_code=HTTP_204_NO_CONTENT)
async def async_response_cookies() -> None:
    pass


@get("/sync-response-cookies", response_cookies=response_cookies, status_code=HTTP_204_NO_CONTENT)
def sync_response_cookies() -> None:
    pass


# url


@get("/async-url-access", status_code=HTTP_204_NO_CONTENT)
async def async_url_access(request: Request) -> None:
    scheme = request.url.scheme
    netloc = request.url.netloc
    path = request.url.path
    fragment = request.url.fragment
    query = request.url.query
    username = request.url.username
    password = request.url.password
    port = request.url.port
    hostname = request.url.hostname
    for key, value in request.query_params.items():
        pass


@get("/sync-url-access", status_code=HTTP_204_NO_CONTENT)
def sync_url_access(request: Request) -> None:
    scheme = request.url.scheme
    netloc = request.url.netloc
    path = request.url.path
    fragment = request.url.fragment
    query = request.url.query
    username = request.url.username
    password = request.url.password
    port = request.url.port
    hostname = request.url.hostname
    for key, value in request.query_params.items():
        pass


# files


@get("/async-file-response-100B")
async def async_file_response_100b() -> File:
    return File(path=data.RESPONSE_FILE_100B, filename="response_file")


@get("/async-file-response-50K")
async def async_file_response_50k() -> File:
    return File(path=data.RESPONSE_FILE_50K, filename="response_file")


@get("/async-file-response-1K")
async def async_file_response_1k() -> File:
    return File(path=data.RESPONSE_FILE_1K, filename="response_file")


@get("/async-file-response-1M")
async def async_file_response_1m() -> File:
    return File(path=data.RESPONSE_FILE_1M, filename="response_file")


@get("/sync-file-response-100B")
def sync_file_response_100b() -> File:
    return File(path=data.RESPONSE_FILE_100B, filename="response_file")


@get("/sync-file-response-50K")
def sync_file_response_50k() -> File:
    return File(path=data.RESPONSE_FILE_50K, filename="response_file")


@get("/sync-file-response-1K")
def sync_file_response_1k() -> File:
    return File(path=data.RESPONSE_FILE_1K, filename="response_file")


@get("/sync-file-response-1M")
def sync_file_response_1m() -> File:
    return File(path=data.RESPONSE_FILE_1M, filename="response_file")


app = Starlite(
    route_handlers=[
        async_plaintext_6k,
        sync_plaintext_6k,
        async_plaintext_70k,
        sync_plaintext_70k,
        #
        async_json_2k,
        sync_json_2k,
        async_json_10k,
        sync_json_10k,
        async_json_450k,
        sync_json_450k,
        #
        async_no_params,
        sync_no_params,
        async_path_params,
        sync_path_params,
        async_query_params,
        sync_query_params,
        async_mixed_params,
        sync_mixed_params,
        #
        async_request_headers,
        sync_request_headers,
        async_response_headers,
        sync_response_headers,
        #
        async_request_cookies,
        sync_request_cookies,
        async_response_cookies,
        sync_response_cookies,
        #
        async_url_access,
        sync_url_access,
        #
        async_file_response_100b,
        sync_file_response_100b,
        async_file_response_1k,
        sync_file_response_1k,
        async_file_response_50k,
        sync_file_response_50k,
        async_file_response_1m,
        sync_file_response_1m,
    ],
    openapi_config=None,
)


def run_spec_test(url: str, spec: EndpointSpec) -> None:
    with TestClient(app=app) as client:
        res = client.get(url, **spec.get("request", {}))
        assert res.status_code == spec["result"]["status_code"]
        if expect_bytes := spec["result"].get("bytes"):
            assert expect_bytes == res.content
        if expect_text := spec["result"].get("text"):
            assert expect_text == res.text
        if expect_json := spec["result"].get("json"):
            assert res.json() == expect_json
