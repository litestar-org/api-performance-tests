import time

import anyio
from fastapi import Depends, FastAPI, Response
from fastapi.responses import FileResponse, PlainTextResponse
from starlette.status import HTTP_204_NO_CONTENT

import test_data

app = FastAPI()


# plaintext async


@app.get("/async-plaintext-100B")
async def async_plaintext_100b() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100B)


@app.get("/async-plaintext-1K")
async def async_plaintext_1k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1K)


@app.get("/async-plaintext-10K")
async def async_plaintext_10k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_10K)


@app.get("/async-plaintext-100K")
async def async_plaintext_100k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100K)


@app.get("/async-plaintext-500K")
async def async_plaintext_500k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_500K)


@app.get("/async-plaintext-1M")
async def async_plaintext_1m() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1M)


@app.get("/async-plaintext-5M")
async def async_plaintext_5m() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_5M)


# plaintext sync


@app.get("/sync-plaintext-100B")
def sync_plaintext_100b() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100B)


@app.get("/sync-plaintext-1K")
def sync_plaintext_1k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1K)


@app.get("/sync-plaintext-10K")
def sync_plaintext_10k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_10K)


@app.get("/sync-plaintext-100K")
def sync_plaintext_100k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100K)


@app.get("/sync-plaintext-500K")
def sync_plaintext_500k() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_500K)


@app.get("/sync-plaintext-1M")
def sync_plaintext_1m() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1M)


@app.get("/sync-plaintext-5M")
def sync_plaintext_5m() -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_5M)


# JSON response


@app.get("/async-json-1K")
async def async_json_1k() -> dict:
    return test_data.JSON_1K


@app.get("/async-json-10K")
async def async_json_10k() -> dict:
    return test_data.JSON_10K


@app.get("/async-json-100K")
async def async_json_100k() -> dict:
    return test_data.JSON_100K


@app.get("/async-json-500K")
async def async_json_500k() -> dict:
    return test_data.JSON_500K


@app.get("/async-json-1M")
async def async_json_1m() -> dict:
    return test_data.JSON_1M


@app.get("/async-json-5M")
async def async_json_5m() -> dict:
    return test_data.JSON_5M


# JSON sync


@app.get("/sync-json-1K")
def sync_json_1k() -> dict:
    return test_data.JSON_1K


@app.get("/sync-json-10K")
def sync_json_10k() -> dict:
    return test_data.JSON_10K


@app.get("/sync-json-100K")
def sync_json_100k() -> dict:
    return test_data.JSON_100K


@app.get("/sync-json-500K")
def sync_json_500k() -> dict:
    return test_data.JSON_500K


@app.get("/sync-json-1M")
def sync_json_1m() -> dict:
    return test_data.JSON_1M


@app.get("/sync-json-5M")
def sync_json_5m() -> dict:
    return test_data.JSON_5M


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


@app.get("/async-response-headers")
async def async_response_headers() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


@app.get("/sync-response-headers")
def sync_response_headers() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


# cookies


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


# files async


@app.get("/async-file-response-100B")
async def async_file_response_100b() -> FileResponse:
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


@app.get("/async-file-response-1K")
async def async_file_response_1k() -> FileResponse:
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


@app.get("/async-file-response-10K")
async def async_file_response_10k() -> FileResponse:
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


@app.get("/async-file-response-100K")
async def async_file_response_100k() -> FileResponse:
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


@app.get("/async-file-response-500K")
async def async_file_response_500k() -> FileResponse:
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


@app.get("/async-file-response-1M")
async def async_file_response_1m() -> FileResponse:
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


@app.get("/async-file-response-5M")
async def async_file_response_5m() -> FileResponse:
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


# files sync


@app.get("/sync-file-response-100B")
def sync_file_response_100b() -> FileResponse:
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


@app.get("/sync-file-response-1K")
def sync_file_response_1k() -> FileResponse:
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


@app.get("/sync-file-response-10K")
def sync_file_response_10k() -> FileResponse:
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


@app.get("/sync-file-response-100K")
def sync_file_response_100k() -> FileResponse:
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


@app.get("/sync-file-response-500K")
def sync_file_response_500k() -> FileResponse:
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


@app.get("/sync-file-response-1M")
def sync_file_response_1m() -> FileResponse:
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


@app.get("/sync-file-response-5M")
def sync_file_response_5m() -> FileResponse:
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


def sync_dependency_one() -> str:
    time.sleep(0.00000001)
    return "sync_dependency_one"


def sync_dependency_two(
    injected_sync_one: str = Depends(sync_dependency_one),  # noqa: B008
) -> list[str]:
    time.sleep(0.00000001)
    return [injected_sync_one, "sync_dependency_two"]


def sync_dependency_three(
    injected_sync_two: list[str] = Depends(sync_dependency_two),  # noqa: B008
) -> list[str]:
    time.sleep(0.00000001)
    return [*injected_sync_two, "sync_dependency_three"]


async def async_dependency_one() -> str:
    await anyio.sleep(0.00000001)
    return "async_dependency_one"


async def async_dependency_two(
    injected_async_one: str = Depends(async_dependency_one),  # noqa: B008
) -> list[str]:
    await anyio.sleep(0.00000001)
    return [injected_async_one, "async_dependency_two"]


async def async_dependency_three(
    injected_async_two: list[str] = Depends(async_dependency_two),  # noqa: B008
) -> list[str]:
    await anyio.sleep(0.00000001)
    return [*injected_async_two, "async_dependency_three"]


async def dependencies_mixed(
    injected_sync_three: list[str] = Depends(sync_dependency_three),  # noqa: B008
    injected_async_three: list[str] = Depends(async_dependency_three),  # noqa: B008
) -> tuple[list[str], list[str]]:
    return injected_sync_three, injected_async_three


@app.get("/sync-dependencies-sync")
def sync_dependencies_sync(
    injected_sync_one: str = Depends(sync_dependency_one),  # noqa: B008
    injected_sync_two: list[str] = Depends(sync_dependency_two),  # noqa: B008
    injected_sync_three: list[str] = Depends(sync_dependency_three),  # noqa: B008
) -> list[str]:
    return injected_sync_three


@app.get("/sync-dependencies-async")
def sync_dependencies_async(
    injected_async_one: str = Depends(async_dependency_one),  # noqa: B008
    injected_async_two: list[str] = Depends(async_dependency_two),  # noqa: B008
    injected_async_three: list[str] = Depends(async_dependency_three),  # noqa: B008
) -> list[str]:
    return injected_async_three


@app.get("/sync-dependencies-mixed")
def sync_dependencies_mixed(
    injected_sync_one: str = Depends(sync_dependency_one),  # noqa: B008
    injected_sync_two: list[str] = Depends(sync_dependency_two),  # noqa: B008
    injected_sync_three: list[str] = Depends(sync_dependency_three),  # noqa: B008
    injected_async_one: str = Depends(async_dependency_one),  # noqa: B008
    injected_async_two: list[str] = Depends(async_dependency_two),  # noqa: B008
    injected_async_three: list[str] = Depends(async_dependency_three),  # noqa: B008
    injected_mixed: tuple[list[str], list[str]] = Depends(dependencies_mixed),  # noqa: B008
) -> tuple[list[str], list[str]]:
    return injected_mixed


@app.get("/async-dependencies-sync")
async def async_dependencies_sync(
    injected_sync_one: str = Depends(sync_dependency_one),  # noqa: B008
    injected_sync_two: list[str] = Depends(sync_dependency_two),  # noqa: B008
    injected_sync_three: list[str] = Depends(sync_dependency_three),  # noqa: B008
) -> list[str]:
    return injected_sync_three


@app.get("/async-dependencies-async")
async def async_dependencies_async(
    injected_async_one: str = Depends(async_dependency_one),  # noqa: B008
    injected_async_two: list[str] = Depends(async_dependency_two),  # noqa: B008
    injected_async_three: list[str] = Depends(async_dependency_three),  # noqa: B008
) -> list[str]:
    return injected_async_three


@app.get("/async-dependencies-mixed")
async def async_dependencies_mixed(
    injected_sync_one: str = Depends(sync_dependency_one),  # noqa: B008
    injected_sync_two: list[str] = Depends(sync_dependency_two),  # noqa: B008
    injected_sync_three: list[str] = Depends(sync_dependency_three),  # noqa: B008
    injected_async_one: str = Depends(async_dependency_one),  # noqa: B008
    injected_async_two: list[str] = Depends(async_dependency_two),  # noqa: B008
    injected_async_three: list[str] = Depends(async_dependency_three),  # noqa: B008
    injected_mixed: tuple[list[str], list[str]] = Depends(dependencies_mixed),  # noqa: B008
) -> tuple[list[str], list[str]]:
    return injected_mixed


# serialize pydantic


@app.get("/sync-serialize-pydantic-50", response_model=list[test_data.objects.PersonPydantic])
def sync_serialize_pydantic_50() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_50


@app.get("/sync-serialize-pydantic-100", response_model=list[test_data.objects.PersonPydantic])
def sync_serialize_pydantic_100() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_100


@app.get("/sync-serialize-pydantic-500", response_model=list[test_data.objects.PersonPydantic])
def sync_serialize_pydantic_500() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_500


@app.get("/async-serialize-pydantic-50", response_model=list[test_data.objects.PersonPydantic])
async def async_serialize_pydantic_50() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_50


@app.get("/async-serialize-pydantic-100", response_model=list[test_data.objects.PersonPydantic])
async def async_serialize_pydantic_100() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_100


@app.get("/async-serialize-pydantic-500", response_model=list[test_data.objects.PersonPydantic])
async def async_serialize_pydantic_500() -> list[test_data.objects.PersonPydantic]:
    return test_data.PERSONS_PYDANTIC_500


# serialize dataclasses


@app.get("/sync-serialize-dataclasses-50", response_model=list[test_data.objects.PersonDataclass])
def sync_serialize_dataclasses_50() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_50


@app.get("/sync-serialize-dataclasses-100", response_model=list[test_data.objects.PersonDataclass])
def sync_serialize_dataclasses_100() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_100


@app.get("/sync-serialize-dataclasses-500", response_model=list[test_data.objects.PersonDataclass])
def sync_serialize_dataclasses_500() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_500


@app.get("/async-serialize-dataclasses-50", response_model=list[test_data.objects.PersonDataclass])
async def async_serialize_dataclasses_50() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_50


@app.get("/async-serialize-dataclasses-100", response_model=list[test_data.objects.PersonDataclass])
async def async_serialize_dataclasses_100() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_100


@app.get("/async-serialize-dataclasses-500", response_model=list[test_data.objects.PersonDataclass])
async def async_serialize_dataclasses_500() -> list[test_data.objects.PersonDataclass]:
    return test_data.PERSONS_DATACLASSES_500
