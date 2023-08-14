import time
from typing import Any

import anyio
from fastapi import Depends, FastAPI, Response, UploadFile
from fastapi.requests import Request
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.responses import ORJSONResponse

from starlette.status import HTTP_204_NO_CONTENT

import test_data

app = FastAPI()


# plaintext async


@app.get("/async-plaintext-100B", response_class=PlainTextResponse)
async def async_plaintext_100b() -> str:
    return test_data.TEXT_100B


@app.get("/async-plaintext-1K", response_class=PlainTextResponse)
async def async_plaintext_1k() -> str:
    return test_data.TEXT_1K


@app.get("/async-plaintext-10K", response_class=PlainTextResponse)
async def async_plaintext_10k() -> str:
    return test_data.TEXT_10K


@app.get("/async-plaintext-100K", response_class=PlainTextResponse)
async def async_plaintext_100k() -> str:
    return test_data.TEXT_100K


@app.get("/async-plaintext-500K", response_class=PlainTextResponse)
async def async_plaintext_500k() -> str:
    return test_data.TEXT_500K


@app.get("/async-plaintext-1M", response_class=PlainTextResponse)
async def async_plaintext_1m() -> str:
    return test_data.TEXT_1M


@app.get("/async-plaintext-5M", response_class=PlainTextResponse)
async def async_plaintext_5m() -> str:
    return test_data.TEXT_5M


# plaintext sync


@app.get("/sync-plaintext-100B", response_class=PlainTextResponse)
def sync_plaintext_100b() -> str:
    return test_data.TEXT_100B


@app.get("/sync-plaintext-1K", response_class=PlainTextResponse)
def sync_plaintext_1k() -> str:
    return test_data.TEXT_1K


@app.get("/sync-plaintext-10K", response_class=PlainTextResponse)
def sync_plaintext_10k() -> str:
    return test_data.TEXT_10K


@app.get("/sync-plaintext-100K", response_class=PlainTextResponse)
def sync_plaintext_100k() -> str:
    return test_data.TEXT_100K


@app.get("/sync-plaintext-500K", response_class=PlainTextResponse)
def sync_plaintext_500k() -> str:
    return test_data.TEXT_500K


@app.get("/sync-plaintext-1M", response_class=PlainTextResponse)
def sync_plaintext_1m() -> str:
    return test_data.TEXT_1M


@app.get("/sync-plaintext-5M", response_class=PlainTextResponse)
def sync_plaintext_5m() -> str:
    return test_data.TEXT_5M


# JSON response


@app.get("/async-json-1K", response_class=ORJSONResponse)
async def async_json_1k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_1K)


@app.get("/async-json-10K", response_class=ORJSONResponse)
async def async_json_10k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_10K)


@app.get("/async-json-100K", response_class=ORJSONResponse)
async def async_json_100k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_100K)


@app.get("/async-json-500K", response_class=ORJSONResponse)
async def async_json_500k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_500K)


@app.get("/async-json-1M", response_class=ORJSONResponse)
async def async_json_1m() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_1M)


@app.get("/async-json-5M", response_class=ORJSONResponse)
async def async_json_5m() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_5M)


# JSON sync


@app.get("/sync-json-1K", response_class=ORJSONResponse)
def sync_json_1k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_1K)


@app.get("/sync-json-10K", response_class=ORJSONResponse)
def sync_json_10k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_10K)


@app.get("/sync-json-100K", response_class=ORJSONResponse)
def sync_json_100k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_100K)


@app.get("/sync-json-500K", response_class=ORJSONResponse)
def sync_json_500k() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_500K)


@app.get("/sync-json-1M", response_class=ORJSONResponse)
def sync_json_1m() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_1M)


@app.get("/sync-json-5M", response_class=ORJSONResponse)
def sync_json_5m() -> list[dict[str, Any]]:
    return ORJSONResponse(test_data.JSON_5M)


# params


@app.get("/async-no-params", status_code=HTTP_204_NO_CONTENT)
async def async_no_params() -> None:
    pass


@app.get("/sync-no-params", status_code=HTTP_204_NO_CONTENT)
def sync_no_params() -> None:
    pass


@app.get("/async-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT)
async def async_path_params(first: int) -> None:
    pass


@app.get("/sync-path-params/{first:int}", status_code=HTTP_204_NO_CONTENT)
def sync_path_params(first: int) -> None:
    pass


@app.get("/async-query-param", status_code=HTTP_204_NO_CONTENT)
async def async_query_params(first: int) -> None:
    pass


@app.get("/sync-query-param", status_code=HTTP_204_NO_CONTENT)
def sync_query_params(first: int) -> None:
    pass


@app.get("/async-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT)
async def async_mixed_params(first: int, second: int) -> None:
    pass


@app.get("/sync-mixed-params/{second:int}", status_code=HTTP_204_NO_CONTENT)
def sync_mixed_params(first: int, second: int) -> None:
    pass


# headers


@app.get("/async-response-headers", status_code=HTTP_204_NO_CONTENT)
async def async_response_headers(response: Response) -> None:
    response.headers.update(test_data.RESPONSE_HEADERS)


@app.get("/sync-response-headers", status_code=HTTP_204_NO_CONTENT)
def sync_response_headers(response: Response) -> None:
    response.headers.update(test_data.RESPONSE_HEADERS)


# cookies


@app.get("/async-response-cookies", status_code=HTTP_204_NO_CONTENT)
async def async_response_cookies(response: Response) -> None:
    for key, value in test_data.RESPONSE_COOKIES.items():
        response.set_cookie(key, value)


@app.get("/sync-response-cookies", status_code=HTTP_204_NO_CONTENT)
def sync_response_cookies(response: Response) -> None:
    for key, value in test_data.RESPONSE_COOKIES.items():
        response.set_cookie(key, value)


# files async


@app.get("/async-file-response-100B")
async def async_file_response_100b():
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


@app.get("/async-file-response-1K")
async def async_file_response_1k():
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


@app.get("/async-file-response-10K")
async def async_file_response_10k():
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


@app.get("/async-file-response-100K")
async def async_file_response_100k():
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


@app.get("/async-file-response-500K")
async def async_file_response_500k():
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


@app.get("/async-file-response-1M")
async def async_file_response_1m():
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


@app.get("/async-file-response-5M")
async def async_file_response_5m():
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


# files sync


@app.get("/sync-file-response-100B")
def sync_file_response_100b():
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


@app.get("/sync-file-response-1K")
def sync_file_response_1k():
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


@app.get("/sync-file-response-10K")
def sync_file_response_10k():
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


@app.get("/sync-file-response-100K")
def sync_file_response_100k():
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


@app.get("/sync-file-response-500K")
def sync_file_response_500k():
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


@app.get("/sync-file-response-1M")
def sync_file_response_1m():
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


@app.get("/sync-file-response-5M")
def sync_file_response_5m():
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


def sync_dependency_one() -> str:
    time.sleep(0.00000001)
    return "sync_dependency_one"


def sync_dependency_two(
    injected_sync_one: str = Depends(sync_dependency_one),
) -> list[str]:
    time.sleep(0.00000001)
    return [injected_sync_one, "sync_dependency_two"]


def sync_dependency_three(
    injected_sync_two: list[str] = Depends(sync_dependency_two),
) -> list[str]:
    time.sleep(0.00000001)
    return [*injected_sync_two, "sync_dependency_three"]


async def async_dependency_one() -> str:
    await anyio.sleep(0.00000001)
    return "async_dependency_one"


async def async_dependency_two(
    injected_async_one: str = Depends(async_dependency_one),
) -> list[str]:
    await anyio.sleep(0.00000001)
    return [injected_async_one, "async_dependency_two"]


async def async_dependency_three(
    injected_async_two: list[str] = Depends(async_dependency_two),
) -> list[str]:
    await anyio.sleep(0.00000001)
    return [*injected_async_two, "async_dependency_three"]


async def dependencies_mixed(
    injected_sync_three: list[str] = Depends(sync_dependency_three),
    injected_async_three: list[str] = Depends(async_dependency_three),
) -> tuple[list[str], list[str]]:
    return injected_sync_three, injected_async_three


@app.get("/sync-dependencies-sync")
def sync_dependencies_sync(
    injected_sync_one: str = Depends(sync_dependency_one),
    injected_sync_two: list[str] = Depends(sync_dependency_two),
    injected_sync_three: list[str] = Depends(sync_dependency_three),
) -> list[str]:
    return injected_sync_three


@app.get("/sync-dependencies-async")
def sync_dependencies_async(
    injected_async_one: str = Depends(async_dependency_one),
    injected_async_two: list[str] = Depends(async_dependency_two),
    injected_async_three: list[str] = Depends(async_dependency_three),
) -> list[str]:
    return injected_async_three


@app.get("/sync-dependencies-mixed")
def sync_dependencies_mixed(
    injected_sync_one: str = Depends(sync_dependency_one),
    injected_sync_two: list[str] = Depends(sync_dependency_two),
    injected_sync_three: list[str] = Depends(sync_dependency_three),
    injected_async_one: str = Depends(async_dependency_one),
    injected_async_two: list[str] = Depends(async_dependency_two),
    injected_async_three: list[str] = Depends(async_dependency_three),
    injected_mixed: tuple[list[str], list[str]] = Depends(dependencies_mixed),
) -> tuple[list[str], list[str]]:
    return injected_mixed


@app.get("/async-dependencies-sync")
async def async_dependencies_sync(
    injected_sync_one: str = Depends(sync_dependency_one),
    injected_sync_two: list[str] = Depends(sync_dependency_two),
    injected_sync_three: list[str] = Depends(sync_dependency_three),
) -> list[str]:
    return injected_sync_three


@app.get("/async-dependencies-async")
async def async_dependencies_async(
    injected_async_one: str = Depends(async_dependency_one),
    injected_async_two: list[str] = Depends(async_dependency_two),
    injected_async_three: list[str] = Depends(async_dependency_three),
) -> list[str]:
    return injected_async_three


@app.get("/async-dependencies-mixed")
async def async_dependencies_mixed(
    injected_sync_one: str = Depends(sync_dependency_one),
    injected_sync_two: list[str] = Depends(sync_dependency_two),
    injected_sync_three: list[str] = Depends(sync_dependency_three),
    injected_async_one: str = Depends(async_dependency_one),
    injected_async_two: list[str] = Depends(async_dependency_two),
    injected_async_three: list[str] = Depends(async_dependency_three),
    injected_mixed: tuple[list[str], list[str]] = Depends(dependencies_mixed),
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


# request body json


@app.post("/sync-post-json", status_code=HTTP_204_NO_CONTENT)
def sync_post_json(data: list) -> None:
    pass


@app.post("/async-post-json", status_code=HTTP_204_NO_CONTENT)
async def async_post_json(data: list) -> None:
    pass


# request body multipart


@app.post("/async-post-multipart-form", status_code=HTTP_204_NO_CONTENT)
async def async_post_multipart_form(request: Request) -> None:
    await request.form()


# form urlencoded


@app.post("/async-post-form-urlencoded", status_code=HTTP_204_NO_CONTENT)
async def async_post_form_urlencoded(request: Request) -> None:
    await request.form()


# upload files


@app.post("/sync-post-file", status_code=HTTP_204_NO_CONTENT)
def sync_post_file(test_file: UploadFile) -> None:
    test_file.file.read()


@app.post("/async-post-file", status_code=HTTP_204_NO_CONTENT)
async def async_post_file(test_file: UploadFile) -> None:
    await test_file.read()
