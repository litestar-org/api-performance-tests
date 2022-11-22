from starlite import Cookie, File, MediaType, ResponseHeader, Starlite, get
from starlite.status_codes import HTTP_204_NO_CONTENT

import test_data

response_headers = {name: ResponseHeader(value=value) for name, value in test_data.RESPONSE_HEADERS.items()}
response_cookies = [Cookie(key=key, value=value) for key, value in test_data.RESPONSE_COOKIES.items()]


@get("/async-plaintext-100B", media_type=MediaType.TEXT)
async def async_plaintext_100b() -> str:
    return test_data.TEXT_100B


@get("/async-plaintext-1K", media_type=MediaType.TEXT)
async def async_plaintext_1k() -> str:
    return test_data.TEXT_1K


@get("/async-plaintext-10K", media_type=MediaType.TEXT)
async def async_plaintext_10k() -> str:
    return test_data.TEXT_10K


@get("/async-plaintext-100K", media_type=MediaType.TEXT)
async def async_plaintext_100k() -> str:
    return test_data.TEXT_100K


@get("/async-plaintext-500K", media_type=MediaType.TEXT)
async def async_plaintext_500k() -> str:
    return test_data.TEXT_500K


@get("/async-plaintext-1M", media_type=MediaType.TEXT)
async def async_plaintext_1m() -> str:
    return test_data.TEXT_1M


@get("/async-plaintext-5M", media_type=MediaType.TEXT)
async def async_plaintext_5m() -> str:
    return test_data.TEXT_5M


# plaintext sync


@get("/sync-plaintext-100B", media_type=MediaType.TEXT)
def sync_plaintext_100b() -> str:
    return test_data.TEXT_100B


@get("/sync-plaintext-1K", media_type=MediaType.TEXT)
def sync_plaintext_1k() -> str:
    return test_data.TEXT_1K


@get("/sync-plaintext-10K", media_type=MediaType.TEXT)
def sync_plaintext_10k() -> str:
    return test_data.TEXT_10K


@get("/sync-plaintext-100K", media_type=MediaType.TEXT)
def sync_plaintext_100k() -> str:
    return test_data.TEXT_100K


@get("/sync-plaintext-500K", media_type=MediaType.TEXT)
def sync_plaintext_500k() -> str:
    return test_data.TEXT_500K


@get("/sync-plaintext-1M", media_type=MediaType.TEXT)
def sync_plaintext_1m() -> str:
    return test_data.TEXT_1M


@get("/sync-plaintext-5M", media_type=MediaType.TEXT)
def sync_plaintext_5m() -> str:
    return test_data.TEXT_5M


# JSON async


@get("/async-json-1K", media_type=MediaType.JSON)
async def async_json_1k() -> dict:
    return test_data.JSON_1K


@get("/async-json-10K", media_type=MediaType.JSON)
async def async_json_10k() -> dict:
    return test_data.JSON_10K


@get("/async-json-100K", media_type=MediaType.JSON)
async def async_json_100k() -> dict:
    return test_data.JSON_100K


@get("/async-json-500K", media_type=MediaType.JSON)
async def async_json_500k() -> dict:
    return test_data.JSON_500K


@get("/async-json-1M", media_type=MediaType.JSON)
async def async_json_1m() -> dict:
    return test_data.JSON_1M


@get("/async-json-5M", media_type=MediaType.JSON)
async def async_json_5m() -> dict:
    return test_data.JSON_5M


# JSON sync


@get("/sync-json-1K", media_type=MediaType.JSON)
def sync_json_1k() -> dict:
    return test_data.JSON_1K


@get("/sync-json-10K", media_type=MediaType.JSON)
def sync_json_10k() -> dict:
    return test_data.JSON_10K


@get("/sync-json-100K", media_type=MediaType.JSON)
def sync_json_100k() -> dict:
    return test_data.JSON_100K


@get("/sync-json-500K", media_type=MediaType.JSON)
def sync_json_500k() -> dict:
    return test_data.JSON_500K


@get("/sync-json-1M", media_type=MediaType.JSON)
def sync_json_1m() -> dict:
    return test_data.JSON_1M


@get("/sync-json-5M", media_type=MediaType.JSON)
def sync_json_5m() -> dict:
    return test_data.JSON_5M


# params


@get("/async-no-params", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_no_params() -> None:
    pass


@get("/sync-no-params", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_no_params() -> None:
    pass


@get("/async-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_path_params(first: int) -> None:
    pass


@get("/sync-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_path_params(first: int) -> None:
    pass


@get("/async-query-param", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_query_params(first: int) -> None:
    pass


@get("/sync-query-param", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_query_params(first: int) -> None:
    pass


@get("/async-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_mixed_params(first: int, second: int) -> None:
    pass


@get("/sync-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_mixed_params(first: int, second: int) -> None:
    pass


@get(
    "/async-response-headers",
    response_headers=response_headers,
    status_code=HTTP_204_NO_CONTENT,
    media_type=MediaType.TEXT,
)
async def async_response_headers() -> None:
    pass


@get(
    "/sync-response-headers",
    response_headers=response_headers,
    status_code=HTTP_204_NO_CONTENT,
    media_type=MediaType.TEXT,
)
def sync_response_headers() -> None:
    pass


# cookies


@get(
    "/async-response-cookies",
    response_cookies=response_cookies,
    status_code=HTTP_204_NO_CONTENT,
    media_type=MediaType.TEXT,
)
async def async_response_cookies() -> None:
    pass


@get(
    "/sync-response-cookies",
    response_cookies=response_cookies,
    status_code=HTTP_204_NO_CONTENT,
    media_type=MediaType.TEXT,
)
def sync_response_cookies() -> None:
    pass


# files async


@get("/async-file-response-100B")
async def async_file_response_100b() -> File:
    return File(path=test_data.FILE_100B, filename="response_file")


@get("/async-file-response-1K")
async def async_file_response_1k() -> File:
    return File(path=test_data.FILE_1K, filename="response_file")


@get("/async-file-response-10K")
async def async_file_response_10k() -> File:
    return File(path=test_data.FILE_10K, filename="response_file")


@get("/async-file-response-100K")
async def async_file_response_100k() -> File:
    return File(path=test_data.FILE_100K, filename="response_file")


@get("/async-file-response-500K")
async def async_file_response_500k() -> File:
    return File(path=test_data.FILE_500K, filename="response_file")


@get("/async-file-response-1M")
async def async_file_response_1m() -> File:
    return File(path=test_data.FILE_1M, filename="response_file")


@get("/async-file-response-5M")
async def async_file_response_5m() -> File:
    return File(path=test_data.FILE_5M, filename="response_file")


# files sync


@get("/sync-file-response-100B")
def sync_file_response_100b() -> File:
    return File(path=test_data.FILE_100B, filename="response_file")


@get("/sync-file-response-1K")
def sync_file_response_1k() -> File:
    return File(path=test_data.FILE_1K, filename="response_file")


@get("/sync-file-response-10K")
def sync_file_response_10k() -> File:
    return File(path=test_data.FILE_10K, filename="response_file")


@get("/sync-file-response-100K")
def sync_file_response_100k() -> File:
    return File(path=test_data.FILE_100K, filename="response_file")


@get("/sync-file-response-500K")
def sync_file_response_500k() -> File:
    return File(path=test_data.FILE_500K, filename="response_file")


@get("/sync-file-response-1M")
def sync_file_response_1m() -> File:
    return File(path=test_data.FILE_1M, filename="response_file")


@get("/sync-file-response-5M")
def sync_file_response_5m() -> File:
    return File(path=test_data.FILE_5M, filename="response_file")


app = Starlite(
    route_handlers=[
        # plaintext async
        async_plaintext_100b,
        async_plaintext_1k,
        async_plaintext_10k,
        async_plaintext_100k,
        async_plaintext_500k,
        async_plaintext_1m,
        async_plaintext_5m,
        # plaintext sync
        sync_plaintext_100b,
        sync_plaintext_1k,
        sync_plaintext_10k,
        sync_plaintext_100k,
        sync_plaintext_500k,
        sync_plaintext_1m,
        sync_plaintext_5m,
        # json async
        async_json_1k,
        async_json_10k,
        async_json_100k,
        async_json_500k,
        async_json_1m,
        async_json_5m,
        # json sync
        sync_json_1k,
        sync_json_10k,
        sync_json_100k,
        sync_json_500k,
        sync_json_1m,
        sync_json_5m,
        # params
        async_no_params,
        sync_no_params,
        async_path_params,
        sync_path_params,
        async_query_params,
        sync_query_params,
        async_mixed_params,
        sync_mixed_params,
        #
        async_response_headers,
        sync_response_headers,
        #
        async_response_cookies,
        sync_response_cookies,
        # files async
        async_file_response_100b,
        async_file_response_1k,
        async_file_response_10k,
        async_file_response_100k,
        async_file_response_500k,
        async_file_response_1m,
        async_file_response_5m,
        # files sync
        sync_file_response_100b,
        sync_file_response_1k,
        sync_file_response_10k,
        sync_file_response_100k,
        sync_file_response_500k,
        sync_file_response_1m,
        sync_file_response_5m,
    ],
    openapi_config=None,
)
