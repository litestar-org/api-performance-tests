from fastapi import FastAPI, Response
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
