import time

from sanic import HTTPResponse, Request, Sanic
from sanic.response import ResponseStream, empty, file, file_stream, json, text

import test_data

app = Sanic("MyApp")


@app.get("/async-plaintext-100B")
async def async_plaintext_100b(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_100B)


@app.get("/async-plaintext-1K")
async def async_plaintext_1k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_1K)


@app.get("/async-plaintext-10K")
async def async_plaintext_10k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_10K)


@app.get("/async-plaintext-100K")
async def async_plaintext_100k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_100K)


@app.get("/async-plaintext-500K")
async def async_plaintext_500k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_500K)


@app.get("/async-plaintext-1M")
async def async_plaintext_1m(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_1M)


@app.get("/async-plaintext-5M")
async def async_plaintext_5m(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_5M)


# plaintext sync


@app.get("/sync-plaintext-100B")
def sync_plaintext_100b(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_100B)


@app.get("/sync-plaintext-1K")
def sync_plaintext_1k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_1K)


@app.get("/sync-plaintext-10K")
def sync_plaintext_10k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_10K)


@app.get("/sync-plaintext-100K")
def sync_plaintext_100k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_100K)


@app.get("/sync-plaintext-500K")
def sync_plaintext_500k(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_500K)


@app.get("/sync-plaintext-1M")
def sync_plaintext_1m(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_1M)


@app.get("/sync-plaintext-5M")
def sync_plaintext_5m(request: Request) -> HTTPResponse:
    return text(test_data.TEXT_5M)


# JSON response


@app.get("/async-json-1K")
async def async_json_1k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_1K)


@app.get("/async-json-10K")
async def async_json_10k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_10K)


@app.get("/async-json-100K")
async def async_json_100k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_100K)


@app.get("/async-json-500K")
async def async_json_500k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_500K)


@app.get("/async-json-1M")
async def async_json_1m(request: Request) -> HTTPResponse:
    return json(test_data.JSON_1M)


@app.get("/async-json-5M")
async def async_json_5m(request: Request) -> HTTPResponse:
    return json(test_data.JSON_5M)


# JSON sync


@app.get("/sync-json-1K")
def sync_json_1k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_1K)


@app.get("/sync-json-10K")
def sync_json_10k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_10K)


@app.get("/sync-json-100K")
def sync_json_100k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_100K)


@app.get("/sync-json-500K")
def sync_json_500k(request: Request) -> HTTPResponse:
    return json(test_data.JSON_500K)


@app.get("/sync-json-1M")
def sync_json_1m(request: Request) -> HTTPResponse:
    return json(test_data.JSON_1M)


@app.get("/sync-json-5M")
def sync_json_5m(request: Request) -> HTTPResponse:
    return json(test_data.JSON_5M)


# params


@app.get("/async-no-params")
async def async_no_params(request: Request) -> HTTPResponse:
    return empty()


@app.get("/sync-no-params")
def sync_no_params(request: Request) -> HTTPResponse:
    return empty()


@app.get("/async-path-params/<first:int>")
async def async_path_params(request: Request, first: int) -> HTTPResponse:
    return empty()


@app.get("/sync-path-params/<first:int>")
def sync_path_params(request: Request, first: int) -> HTTPResponse:
    return empty()


@app.get("/async-query-param")
async def async_query_params(request: Request) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


@app.get("/sync-query-param")
def sync_query_params(request: Request) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


@app.get("/async-mixed-params/<second:int>")
async def async_mixed_params(request: Request, second: int) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


@app.get("/sync-mixed-params/<second:int>")
def sync_mixed_params(request: Request, second: int) -> HTTPResponse:
    int(request.args.get("first"))
    return empty()


# headers


@app.get("/async-response-headers")
async def async_response_headers(request: Request) -> HTTPResponse:
    return empty(headers=test_data.RESPONSE_HEADERS)


@app.get("/sync-response-headers")
def sync_response_headers(request: Request) -> HTTPResponse:
    return empty(headers=test_data.RESPONSE_HEADERS)


# cookies


@app.get("/async-response-cookies")
async def async_response_cookies(request: Request) -> HTTPResponse:
    res = empty()
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.cookies[key] = value
    return res


@app.get("/sync-response-cookies")
def sync_response_cookies(request: Request) -> HTTPResponse:
    res = empty()
    for key, value in test_data.RESPONSE_COOKIES.items():
        res.cookies[key] = value
    return res


# files


@app.get("/async-file-response-100B")
async def async_file_response_100b(request: Request) -> HTTPResponse:
    return await file(location=test_data.FILE_100B, filename="response_file")


@app.get("/async-file-response-1K")
async def async_file_response_1k(request: Request) -> HTTPResponse:
    return await file(location=test_data.FILE_1K, filename="response_file")


@app.get("/async-file-response-10K")
async def async_file_response_10k(request: Request) -> HTTPResponse:
    return await file(location=test_data.FILE_10K, filename="response_file")


@app.get("/async-file-response-100K")
async def async_file_response_100k(request: Request) -> ResponseStream:
    return await file_stream(location=test_data.FILE_100K, filename="response_file")


@app.get("/async-file-response-500K")
async def async_file_response_500k(request: Request) -> ResponseStream:
    return await file_stream(location=test_data.FILE_500K, filename="response_file")


@app.get("/async-file-response-1M")
async def async_file_response_1m(request: Request) -> ResponseStream:
    return await file_stream(location=test_data.FILE_1M, filename="response_file")


@app.get("/async-file-response-5M")
async def async_file_response_5m(request: Request) -> ResponseStream:
    return await file_stream(location=test_data.FILE_5M, filename="response_file")


# files sync


class SyncDependencyOne:
    def __init__(self) -> None:
        time.sleep(0.00000001)
        self.value = "sync_dependency_one"


class SyncDependencyTwo:
    def __init__(self, one: SyncDependencyOne) -> None:
        time.sleep(0.00000001)
        self.value = [one.value, "sync_dependency_two"]


class SyncDependencyThree:
    def __init__(self, two: SyncDependencyTwo) -> None:
        time.sleep(0.00000001)
        self.value = [*two.value, "sync_dependency_three"]


app.ext.add_dependency(SyncDependencyOne)
app.ext.add_dependency(SyncDependencyTwo)
app.ext.add_dependency(SyncDependencyThree)


@app.get("/sync-dependencies-sync")
def sync_dependencies_sync(
    request: Request,
    injected_sync_one: SyncDependencyOne,
    injected_sync_two: SyncDependencyTwo,
    injected_sync_three: SyncDependencyThree,
) -> HTTPResponse:
    return json(injected_sync_three.value)


@app.get("/async-dependencies-sync")
async def async_dependencies_sync(
    request: Request,
    injected_sync_one: SyncDependencyOne,
    injected_sync_two: SyncDependencyTwo,
    injected_sync_three: SyncDependencyThree,
) -> HTTPResponse:
    return json(injected_sync_three.value)


# request body json


@app.post("/sync-post-json")
def sync_post_json(request: Request) -> HTTPResponse:
    return empty()


@app.post("/async-post-json")
async def async_post_json(request: Request) -> HTTPResponse:
    return empty()


# request body multipart


@app.post("/sync-post-multipart-form")
def sync_post_multipart_form(request: Request) -> HTTPResponse:
    return empty()


@app.post("/async-post-multipart-form")
async def async_post_multipart_form(request: Request) -> HTTPResponse:
    return empty()


# form urlencoded


@app.post("/sync-post-form-urlencoded")
def sync_post_form_urlencoded(request: Request) -> HTTPResponse:
    return empty()


@app.post("/async-post-form-urlencoded")
async def async_post_form_urlencoded(request: Request) -> HTTPResponse:
    return empty()


# upload files


@app.post("/sync-post-file")
def sync_post_file(request: Request) -> HTTPResponse:
    request.files.get("test_file").body
    return empty()


@app.post("/async-post-file")
async def async_post_file(request: Request) -> HTTPResponse:
    request.files.get("test_file").body
    return empty()
