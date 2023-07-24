import time
from typing import Any

import anyio
from starlite import (
    Body,
    Cookie,
    File,
    MediaType,
    Provide,
    RequestEncodingType,
    ResponseHeader,
    Starlite,
    UploadFile,
    get,
    post,
)
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
async def async_json_1k() -> list[dict[str, Any]]:
    return test_data.JSON_1K


@get("/async-json-10K", media_type=MediaType.JSON)
async def async_json_10k() -> list[dict[str, Any]]:
    return test_data.JSON_10K


@get("/async-json-100K", media_type=MediaType.JSON)
async def async_json_100k() -> list[dict[str, Any]]:
    return test_data.JSON_100K


@get("/async-json-500K", media_type=MediaType.JSON)
async def async_json_500k() -> list[dict[str, Any]]:
    return test_data.JSON_500K


@get("/async-json-1M", media_type=MediaType.JSON)
async def async_json_1m() -> list[dict[str, Any]]:
    return test_data.JSON_1M


@get("/async-json-5M", media_type=MediaType.JSON)
async def async_json_5m() -> list[dict[str, Any]]:
    return test_data.JSON_5M


# JSON sync


@get("/sync-json-1K", media_type=MediaType.JSON)
def sync_json_1k() -> list[dict[str, Any]]:
    return test_data.JSON_1K


@get("/sync-json-10K", media_type=MediaType.JSON)
def sync_json_10k() -> list[dict[str, Any]]:
    return test_data.JSON_10K


@get("/sync-json-100K", media_type=MediaType.JSON)
def sync_json_100k() -> list[dict[str, Any]]:
    return test_data.JSON_100K


@get("/sync-json-500K", media_type=MediaType.JSON)
def sync_json_500k() -> list[dict[str, Any]]:
    return test_data.JSON_500K


@get("/sync-json-1M", media_type=MediaType.JSON)
def sync_json_1m() -> list[dict[str, Any]]:
    return test_data.JSON_1M


@get("/sync-json-5M", media_type=MediaType.JSON)
def sync_json_5m() -> list[dict[str, Any]]:
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


# dependency injection


def sync_dependency_one() -> str:
    time.sleep(0.00000001)
    return "sync_dependency_one"


def sync_dependency_two(injected_sync_one: str) -> list[str]:
    time.sleep(0.00000001)
    return [injected_sync_one, "sync_dependency_two"]


def sync_dependency_three(injected_sync_two: list[str]) -> list[str]:
    time.sleep(0.00000001)
    return [*injected_sync_two, "sync_dependency_three"]


async def async_dependency_one() -> str:
    await anyio.sleep(0.00000001)
    return "async_dependency_one"


async def async_dependency_two(injected_async_one: str) -> list[str]:
    await anyio.sleep(0.00000001)
    return [injected_async_one, "async_dependency_two"]


async def async_dependency_three(injected_async_two: list[str]) -> list[str]:
    await anyio.sleep(0.00000001)
    return [*injected_async_two, "async_dependency_three"]


async def dependencies_mixed(
    injected_sync_three: list[str], injected_async_three: list[str]
) -> tuple[list[str], list[str]]:
    return injected_sync_three, injected_async_three


_DEPENDENCIES_SYNC = {
    "injected_sync_one": Provide(sync_dependency_one),
    "injected_sync_two": Provide(sync_dependency_two),
    "injected_sync_three": Provide(sync_dependency_three),
}

_DEPENDENCIES_ASYNC = {
    "injected_async_one": Provide(async_dependency_one),
    "injected_async_two": Provide(async_dependency_two),
    "injected_async_three": Provide(async_dependency_three),
}


@get("/sync-dependencies-sync", dependencies=_DEPENDENCIES_SYNC)
def sync_dependencies_sync(
    injected_sync_one: str, injected_sync_two: list[str], injected_sync_three: list[str]
) -> list[str]:
    return injected_sync_three


@get("/sync-dependencies-async", dependencies=_DEPENDENCIES_ASYNC)
def sync_dependencies_async(
    injected_async_one: str, injected_async_two: list[str], injected_async_three: list[str]
) -> list[str]:
    return injected_async_three


@get(
    "/sync-dependencies-mixed",
    dependencies={
        **_DEPENDENCIES_SYNC,
        **_DEPENDENCIES_ASYNC,
        "injected_mixed": Provide(dependencies_mixed),
    },
)
def sync_dependencies_mixed(
    injected_sync_one: str,
    injected_sync_two: list[str],
    injected_sync_three: list[str],
    injected_async_one: str,
    injected_async_two: list[str],
    injected_async_three: list[str],
    injected_mixed: tuple[list[str], list[str]],
) -> tuple[list[str], list[str]]:
    return injected_mixed


@get("/async-dependencies-sync", dependencies=_DEPENDENCIES_SYNC)
async def async_dependencies_sync(
    injected_sync_one: str, injected_sync_two: list[str], injected_sync_three: list[str]
) -> list[str]:
    return injected_sync_three


@get("/async-dependencies-async", dependencies=_DEPENDENCIES_ASYNC)
async def async_dependencies_async(
    injected_async_one: str, injected_async_two: list[str], injected_async_three: list[str]
) -> list[str]:
    return injected_async_three


@get(
    "/async-dependencies-mixed",
    dependencies={
        **_DEPENDENCIES_SYNC,
        **_DEPENDENCIES_ASYNC,
        "injected_mixed": Provide(dependencies_mixed),
    },
)
async def async_dependencies_mixed(
    injected_sync_one: str,
    injected_sync_two: list[str],
    injected_sync_three: list[str],
    injected_async_one: str,
    injected_async_two: list[str],
    injected_async_three: list[str],
    injected_mixed: tuple[list[str], list[str]],
) -> tuple[list[str], list[str]]:
    return injected_mixed


# serialize pydantic


@get("/sync-serialize-pydantic-50")
def sync_serialize_pydantic_50() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_50


@get("/sync-serialize-pydantic-100")
def sync_serialize_pydantic_100() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_100


@get("/sync-serialize-pydantic-500")
def sync_serialize_pydantic_500() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_500


@get("/async-serialize-pydantic-50")
async def async_serialize_pydantic_50() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_50


@get("/async-serialize-pydantic-100")
async def async_serialize_pydantic_100() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_100


@get("/async-serialize-pydantic-500")
async def async_serialize_pydantic_500() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_500


# serialize dataclasses


@get("/sync-serialize-dataclasses-50")
def sync_serialize_dataclasses_50() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_50


@get("/sync-serialize-dataclasses-100")
def sync_serialize_dataclasses_100() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_100


@get("/sync-serialize-dataclasses-500")
def sync_serialize_dataclasses_500() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_500


@get("/async-serialize-dataclasses-50")
async def async_serialize_dataclasses_50() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_50


@get("/async-serialize-dataclasses-100")
async def async_serialize_dataclasses_100() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_100


@get("/async-serialize-dataclasses-500")
async def async_serialize_dataclasses_500() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_500


# request body json


@post("/sync-post-json", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_post_json(data: list) -> None:
    pass


@post("/async-post-json", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_post_json(data: list) -> None:
    pass


# request body multipart


@post("/sync-post-multipart-form", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_post_multipart_form(data: dict = Body(media_type=RequestEncodingType.MULTI_PART)) -> None:
    pass


@post("/async-post-multipart-form", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_post_multipart_form(data: dict = Body(media_type=RequestEncodingType.MULTI_PART)) -> None:
    pass


# form urlencoded


@post("/sync-post-form-urlencoded", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_post_form_urlencoded(data: dict = Body(media_type=RequestEncodingType.URL_ENCODED)) -> None:
    pass


@post("/async-post-form-urlencoded", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_post_form_urlencoded(data: dict = Body(media_type=RequestEncodingType.URL_ENCODED)) -> None:
    pass


# upload files


@post("/sync-post-file", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
def sync_post_file(data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART)) -> None:
    data.file.read()


@post("/async-post-file", status_code=HTTP_204_NO_CONTENT, media_type=MediaType.TEXT)
async def async_post_file(data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART)) -> None:
    await data.read()


app = Starlite(
    route_handlers=[
        # DI sync
        sync_dependencies_sync,
        sync_dependencies_async,
        sync_dependencies_mixed,
        # DI async
        async_dependencies_sync,
        async_dependencies_async,
        async_dependencies_mixed,
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
        # serialize pydantic
        sync_serialize_pydantic_100,
        sync_serialize_pydantic_50,
        async_serialize_pydantic_100,
        async_serialize_pydantic_50,
        async_serialize_pydantic_500,
        sync_serialize_pydantic_500,
        # serialize dataclasses
        sync_serialize_dataclasses_100,
        sync_serialize_dataclasses_50,
        async_serialize_dataclasses_100,
        async_serialize_dataclasses_50,
        async_serialize_dataclasses_500,
        sync_serialize_dataclasses_500,
        # request bodies
        sync_post_json,
        async_post_json,
        sync_post_multipart_form,
        async_post_multipart_form,
        sync_post_form_urlencoded,
        async_post_form_urlencoded,
        sync_post_file,
        async_post_file,
    ],
    openapi_config=None,
)
