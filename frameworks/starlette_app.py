from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from starlette.status import HTTP_204_NO_CONTENT

import test_data

app = Starlette()

# plaintext async


@app.route("/async-plaintext-100B")
async def async_plaintext_100b(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100B)


@app.route("/async-plaintext-1K")
async def async_plaintext_1k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1K)


@app.route("/async-plaintext-10K")
async def async_plaintext_10k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_10K)


@app.route("/async-plaintext-100K")
async def async_plaintext_100k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100K)


@app.route("/async-plaintext-500K")
async def async_plaintext_500k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_500K)


@app.route("/async-plaintext-1M")
async def async_plaintext_1m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1M)


@app.route("/async-plaintext-5M")
async def async_plaintext_5m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_5M)


# plaintext sync


@app.route("/sync-plaintext-100B")
def sync_plaintext_100b(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100B)


@app.route("/sync-plaintext-1K")
def sync_plaintext_1k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1K)


@app.route("/sync-plaintext-10K")
def sync_plaintext_10k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_10K)


@app.route("/sync-plaintext-100K")
def sync_plaintext_100k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100K)


@app.route("/sync-plaintext-500K")
def sync_plaintext_500k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_500K)


@app.route("/sync-plaintext-1M")
def sync_plaintext_1m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1M)


@app.route("/sync-plaintext-5M")
def sync_plaintext_5m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_5M)


# JSON response


@app.route("/async-json-1K")
async def async_json_1k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1K)


@app.route("/async-json-10K")
async def async_json_10k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_10K)


@app.route("/async-json-100K")
async def async_json_100k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_100K)


@app.route("/async-json-500K")
async def async_json_500k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_500K)


@app.route("/async-json-1M")
async def async_json_1m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1M)


@app.route("/async-json-5M")
async def async_json_5m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_5M)


# JSON sync


@app.route("/sync-json-1K")
def sync_json_1k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1K)


@app.route("/sync-json-10K")
def sync_json_10k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_10K)


@app.route("/sync-json-100K")
def sync_json_100k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_100K)


@app.route("/sync-json-500K")
def sync_json_500k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_500K)


@app.route("/sync-json-1M")
def sync_json_1m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1M)


@app.route("/sync-json-5M")
def sync_json_5m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_5M)


# params


@app.route("/async-no-params")
async def async_no_params(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.route("/sync-no-params")
def sync_no_params(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.route("/async-path-params/{first:int}")
async def async_path_params(request: Request) -> Response:
    int(request.path_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.route("/sync-path-params/{first:int}")
def sync_path_params(request: Request) -> Response:
    int(request.path_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.route("/async-query-param")
async def async_query_params(request: Request) -> Response:
    int(request.query_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.route("/sync-query-param")
def sync_query_params(request: Request) -> Response:
    int(request.query_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.route("/async-mixed-params/{second:int}")
async def async_mixed_params(request: Request) -> Response:
    int(request.query_params["first"])
    request.path_params["second"]
    return Response(status_code=HTTP_204_NO_CONTENT)


@app.route("/sync-mixed-params/{second:int}")
def sync_mixed_params(request: Request) -> Response:
    int(request.query_params["first"])
    request.path_params["second"]
    return Response(status_code=HTTP_204_NO_CONTENT)


# headers


@app.route("/async-response-headers")
async def async_response_headers(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


@app.route("/sync-response-headers")
def sync_response_headers(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


# cookies


@app.route("/async-response-cookies")
async def async_response_cookies(request: Request) -> Response:
    res = Response(status_code=HTTP_204_NO_CONTENT)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


@app.route("/sync-response-cookies")
def sync_response_cookies(request: Request) -> Response:
    res = Response(status_code=HTTP_204_NO_CONTENT)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


# files


@app.route("/async-file-response-100B")
async def async_file_response_100b(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


@app.route("/async-file-response-1K")
async def async_file_response_1k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


@app.route("/async-file-response-10K")
async def async_file_response_10k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


@app.route("/async-file-response-100K")
async def async_file_response_100k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


@app.route("/async-file-response-500K")
async def async_file_response_500k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


@app.route("/async-file-response-1M")
async def async_file_response_1m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


@app.route("/async-file-response-5M")
async def async_file_response_5m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


# files sync


@app.route("/sync-file-response-100B")
def sync_file_response_100b(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


@app.route("/sync-file-response-1K")
def sync_file_response_1k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


@app.route("/sync-file-response-10K")
def sync_file_response_10k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


@app.route("/sync-file-response-100K")
def sync_file_response_100k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


@app.route("/sync-file-response-500K")
def sync_file_response_500k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


@app.route("/sync-file-response-1M")
def sync_file_response_1m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


@app.route("/sync-file-response-5M")
def sync_file_response_5m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


# request body json


@app.route("/async-post-json", methods=["POST"])
async def async_post_json(request: Request) -> Response:
    data = await request.json()
    return Response(status_code=HTTP_204_NO_CONTENT)


# request body multipart


@app.route("/async-post-multipart-form", methods=["POST"])
async def async_post_multipart_form(request: Request) -> Response:
    data = await request.form()
    return Response(status_code=HTTP_204_NO_CONTENT)


# form urlencoded


@app.route("/async-post-form-urlencoded", methods=["POST"])
async def async_post_form_urlencoded(request: Request) -> Response:
    data = await request.form()
    return Response(status_code=HTTP_204_NO_CONTENT)


# upload files


@app.route("/async-post-file", methods=["POST"])
async def async_post_file(request: Request) -> Response:
    form = await request.form()
    content = await form["test_file"].read()
    return Response(status_code=HTTP_204_NO_CONTENT)
