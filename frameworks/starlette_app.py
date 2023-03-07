from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from starlette.routing import Route
from starlette.status import HTTP_204_NO_CONTENT

import test_data

# plaintext async


async def async_plaintext_100b(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100B)


async def async_plaintext_1k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1K)


async def async_plaintext_10k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_10K)


async def async_plaintext_100k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100K)


async def async_plaintext_500k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_500K)


async def async_plaintext_1m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1M)


async def async_plaintext_5m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_5M)


# plaintext sync


def sync_plaintext_100b(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100B)


def sync_plaintext_1k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1K)


def sync_plaintext_10k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_10K)


def sync_plaintext_100k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_100K)


def sync_plaintext_500k(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_500K)


def sync_plaintext_1m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_1M)


def sync_plaintext_5m(request: Request) -> PlainTextResponse:
    return PlainTextResponse(test_data.TEXT_5M)


# JSON response


async def async_json_1k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1K)


async def async_json_10k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_10K)


async def async_json_100k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_100K)


async def async_json_500k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_500K)


async def async_json_1m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1M)


async def async_json_5m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_5M)


# JSON sync


def sync_json_1k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1K)


def sync_json_10k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_10K)


def sync_json_100k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_100K)


def sync_json_500k(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_500K)


def sync_json_1m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_1M)


def sync_json_5m(request: Request) -> JSONResponse:
    return JSONResponse(test_data.JSON_5M)


# params


async def async_no_params(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


def sync_no_params(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)


async def async_path_params(request: Request) -> Response:
    int(request.path_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


def sync_path_params(request: Request) -> Response:
    int(request.path_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


async def async_query_params(request: Request) -> Response:
    int(request.query_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


def sync_query_params(request: Request) -> Response:
    int(request.query_params["first"])
    return Response(status_code=HTTP_204_NO_CONTENT)


async def async_mixed_params(request: Request) -> Response:
    int(request.query_params["first"])
    request.path_params["second"]
    return Response(status_code=HTTP_204_NO_CONTENT)


def sync_mixed_params(request: Request) -> Response:
    int(request.query_params["first"])
    request.path_params["second"]
    return Response(status_code=HTTP_204_NO_CONTENT)


# headers


async def async_response_headers(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


def sync_response_headers(request: Request) -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT, headers=test_data.RESPONSE_HEADERS)


# cookies


async def async_response_cookies(request: Request) -> Response:
    res = Response(status_code=HTTP_204_NO_CONTENT)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


def sync_response_cookies(request: Request) -> Response:
    res = Response(status_code=HTTP_204_NO_CONTENT)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


# files


async def async_file_response_100b(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


async def async_file_response_1k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


async def async_file_response_10k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


async def async_file_response_100k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


async def async_file_response_500k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


async def async_file_response_1m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


async def async_file_response_5m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


# files sync


def sync_file_response_100b(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100B, filename="response_file")


def sync_file_response_1k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1K, filename="response_file")


def sync_file_response_10k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_10K, filename="response_file")


def sync_file_response_100k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_100K, filename="response_file")


def sync_file_response_500k(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_500K, filename="response_file")


def sync_file_response_1m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_1M, filename="response_file")


def sync_file_response_5m(request: Request) -> FileResponse:
    return FileResponse(path=test_data.FILE_5M, filename="response_file")


# request body json


async def async_post_json(request: Request) -> Response:
    data = await request.json()
    return Response(status_code=HTTP_204_NO_CONTENT)


# request body multipart


async def async_post_multipart_form(request: Request) -> Response:
    data = await request.form()
    return Response(status_code=HTTP_204_NO_CONTENT)


# form urlencoded


async def async_post_form_urlencoded(request: Request) -> Response:
    data = await request.form()
    return Response(status_code=HTTP_204_NO_CONTENT)


# upload files


async def async_post_file(request: Request) -> Response:
    form = await request.form()
    content = await form["test_file"].read()
    return Response(status_code=HTTP_204_NO_CONTENT)


app = Starlette(
    routes=[
        Route(path="/async-plaintext-100B", endpoint=async_plaintext_100b, methods=["GET"]),
        Route(path="/async-plaintext-1K", endpoint=async_plaintext_1k, methods=["GET"]),
        Route(path="/async-plaintext-10K", endpoint=async_plaintext_10k, methods=["GET"]),
        Route(path="/async-plaintext-100K", endpoint=async_plaintext_100k, methods=["GET"]),
        Route(path="/async-plaintext-500K", endpoint=async_plaintext_500k, methods=["GET"]),
        Route(path="/async-plaintext-1M", endpoint=async_plaintext_1m, methods=["GET"]),
        Route(path="/async-plaintext-5M", endpoint=async_plaintext_5m, methods=["GET"]),
        Route(path="/sync-plaintext-100B", endpoint=sync_plaintext_100b, methods=["GET"]),
        Route(path="/sync-plaintext-1K", endpoint=sync_plaintext_1k, methods=["GET"]),
        Route(path="/sync-plaintext-10K", endpoint=sync_plaintext_10k, methods=["GET"]),
        Route(path="/sync-plaintext-100K", endpoint=sync_plaintext_100k, methods=["GET"]),
        Route(path="/sync-plaintext-500K", endpoint=sync_plaintext_500k, methods=["GET"]),
        Route(path="/sync-plaintext-1M", endpoint=sync_plaintext_1m, methods=["GET"]),
        Route(path="/sync-plaintext-5M", endpoint=sync_plaintext_5m, methods=["GET"]),
        Route(path="/async-json-1K", endpoint=async_json_1k, methods=["GET"]),
        Route(path="/async-json-10K", endpoint=async_json_10k, methods=["GET"]),
        Route(path="/async-json-100K", endpoint=async_json_100k, methods=["GET"]),
        Route(path="/async-json-500K", endpoint=async_json_500k, methods=["GET"]),
        Route(path="/async-json-1M", endpoint=async_json_1m, methods=["GET"]),
        Route(path="/async-json-5M", endpoint=async_json_5m, methods=["GET"]),
        Route(path="/sync-json-1K", endpoint=sync_json_1k, methods=["GET"]),
        Route(path="/sync-json-10K", endpoint=sync_json_10k, methods=["GET"]),
        Route(path="/sync-json-100K", endpoint=sync_json_100k, methods=["GET"]),
        Route(path="/sync-json-500K", endpoint=sync_json_500k, methods=["GET"]),
        Route(path="/sync-json-1M", endpoint=sync_json_1m, methods=["GET"]),
        Route(path="/sync-json-5M", endpoint=sync_json_5m, methods=["GET"]),
        Route(path="/async-no-params", endpoint=async_no_params, methods=["GET"]),
        Route(path="/sync-no-params", endpoint=sync_no_params, methods=["GET"]),
        Route(path="/async-path-params/{first:int}", endpoint=async_path_params, methods=["GET"]),
        Route(path="/sync-path-params/{first:int}", endpoint=sync_path_params, methods=["GET"]),
        Route(path="/async-query-param", endpoint=async_query_params, methods=["GET"]),
        Route(path="/sync-query-param", endpoint=sync_query_params, methods=["GET"]),
        Route(path="/async-mixed-params/{second:int}", endpoint=async_mixed_params, methods=["GET"]),
        Route(path="/sync-mixed-params/{second:int}", endpoint=sync_mixed_params, methods=["GET"]),
        Route(path="/async-response-headers", endpoint=async_response_headers, methods=["GET"]),
        Route(path="/sync-response-headers", endpoint=sync_response_headers, methods=["GET"]),
        Route(path="/async-response-cookies", endpoint=async_response_cookies, methods=["GET"]),
        Route(path="/sync-response-cookies", endpoint=sync_response_cookies, methods=["GET"]),
        Route(path="/async-file-response-100B", endpoint=async_file_response_100b, methods=["GET"]),
        Route(path="/async-file-response-1K", endpoint=async_file_response_1k, methods=["GET"]),
        Route(path="/async-file-response-10K", endpoint=async_file_response_10k, methods=["GET"]),
        Route(path="/async-file-response-100K", endpoint=async_file_response_100k, methods=["GET"]),
        Route(path="/async-file-response-500K", endpoint=async_file_response_500k, methods=["GET"]),
        Route(path="/async-file-response-1M", endpoint=async_file_response_1m, methods=["GET"]),
        Route(path="/async-file-response-5M", endpoint=async_file_response_5m, methods=["GET"]),
        Route(path="/sync-file-response-100B", endpoint=sync_file_response_100b, methods=["GET"]),
        Route(path="/sync-file-response-1K", endpoint=sync_file_response_1k, methods=["GET"]),
        Route(path="/sync-file-response-10K", endpoint=sync_file_response_10k, methods=["GET"]),
        Route(path="/sync-file-response-100K", endpoint=sync_file_response_100k, methods=["GET"]),
        Route(path="/sync-file-response-500K", endpoint=sync_file_response_500k, methods=["GET"]),
        Route(path="/sync-file-response-1M", endpoint=sync_file_response_1m, methods=["GET"]),
        Route(path="/sync-file-response-5M", endpoint=sync_file_response_5m, methods=["GET"]),
        Route(path="/async-post-json", endpoint=async_post_json, methods=["POST"]),
        Route(path="/async-post-multipart-form", endpoint=async_post_multipart_form, methods=["POST"]),
        Route(path="/async-post-form-urlencoded", endpoint=async_post_form_urlencoded, methods=["POST"]),
        Route(path="/async-post-file", endpoint=async_post_file, methods=["POST"]),
    ]
)
