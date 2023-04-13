import test_data
from quart import Quart, Response, request, send_file

app = Quart(__name__)

# plaintext async


@app.get("/async-plaintext-100B")
async def async_plaintext_100b() -> str:
    return test_data.TEXT_100B


@app.get("/async-plaintext-1K")
async def async_plaintext_1k() -> str:
    return test_data.TEXT_1K


@app.get("/async-plaintext-10K")
async def async_plaintext_10k() -> str:
    return test_data.TEXT_10K


@app.get("/async-plaintext-100K")
async def async_plaintext_100k() -> str:
    return test_data.TEXT_100K


@app.get("/async-plaintext-500K")
async def async_plaintext_500k() -> str:
    return test_data.TEXT_500K


@app.get("/async-plaintext-1M")
async def async_plaintext_1m() -> str:
    return test_data.TEXT_1M


@app.get("/async-plaintext-5M")
async def async_plaintext_5m() -> str:
    return test_data.TEXT_5M


# plaintext sync


@app.get("/sync-plaintext-100B")
def sync_plaintext_100b() -> str:
    return test_data.TEXT_100B


@app.get("/sync-plaintext-1K")
def sync_plaintext_1k() -> str:
    return test_data.TEXT_1K


@app.get("/sync-plaintext-10K")
def sync_plaintext_10k() -> str:
    return test_data.TEXT_10K


@app.get("/sync-plaintext-100K")
def sync_plaintext_100k() -> str:
    return test_data.TEXT_100K


@app.get("/sync-plaintext-500K")
def sync_plaintext_500k() -> str:
    return test_data.TEXT_500K


@app.get("/sync-plaintext-1M")
def sync_plaintext_1m() -> str:
    return test_data.TEXT_1M


@app.get("/sync-plaintext-5M")
def sync_plaintext_5m() -> str:
    return test_data.TEXT_5M


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


@app.get("/async-no-params")
async def async_no_params() -> Response:
    return Response(status=204)


@app.get("/sync-no-params")
def sync_no_params() -> Response:
    return Response(status=204)


@app.get("/async-path-params/<int:first>")
async def async_path_params(first: int) -> Response:
    return Response(status=204)


@app.get("/sync-path-params/<int:first>")
def sync_path_params(first: int) -> Response:
    return Response(status=204)


@app.get("/async-query-param")
async def async_query_params() -> Response:
    request.args.get("first", type=int)
    return Response(status=204)


@app.get("/sync-query-param")
def sync_query_params() -> Response:
    request.args.get("first", type=int)
    return Response(status=204)


@app.get("/async-mixed-params/<int:second>")
async def async_mixed_params(second: int) -> Response:
    request.args.get("first", type=int)
    return Response(status=204)


@app.get("/sync-mixed-params/<int:second>")
def sync_mixed_params(second: int) -> Response:
    request.args.get("first", type=int)
    return Response(status=204)


# headers


@app.get("/async-response-headers")
async def async_response_headers() -> Response:
    return Response(status=204, headers=test_data.RESPONSE_HEADERS)


@app.get("/sync-response-headers")
def sync_response_headers() -> Response:
    return Response(status=204, headers=test_data.RESPONSE_HEADERS)


# cookies


@app.get("/async-response-cookies")
async def async_response_cookies() -> Response:
    res = Response(status=204)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


@app.get("/sync-response-cookies")
def sync_response_cookies() -> Response:
    res = Response(status=204)
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.set_cookie(key, value)
    return res


# files async


@app.get("/async-file-response-100B")
async def async_file_response_100b() -> Response:
    return await send_file(test_data.FILE_100B)


@app.get("/async-file-response-1K")
async def async_file_response_1k() -> Response:
    return await send_file(test_data.FILE_1K)


@app.get("/async-file-response-10K")
async def async_file_response_10k() -> Response:
    return await send_file(test_data.FILE_10K)


@app.get("/async-file-response-100K")
async def async_file_response_100k() -> Response:
    return await send_file(test_data.FILE_100K)


@app.get("/async-file-response-500K")
async def async_file_response_500k() -> Response:
    return await send_file(test_data.FILE_500K)


@app.get("/async-file-response-1M")
async def async_file_response_1m() -> Response:
    return await send_file(test_data.FILE_1M)


@app.get("/async-file-response-5M")
async def async_file_response_5m() -> Response:
    return await send_file(test_data.FILE_5M)


# request body json


@app.post("/async-post-json")
async def async_post_json() -> Response:
    await request.get_json()
    return Response(status=204)


# request body multipart


@app.post("/async-post-multipart-form")
async def async_post_multipart_form() -> Response:
    await request.get_data(parse_form_data=True)
    return Response(status=204)


@app.post("/async-post-form-urlencoded")
async def async_post_form_urlencoded() -> Response:
    await request.get_data(parse_form_data=True)
    return Response(status=204)


# upload files


@app.post("/async-post-file")
async def async_post_file() -> Response:
    await request.files
    return Response(status=204)
