import time

import anyio
from blacksheep import Application, Cookie, FromForm, Request, Response, json, text
from blacksheep.server.responses import file, no_content

import test_data

RESPONSE_COOKIES = [Cookie(name=name, value=value) for name, value in test_data.RESPONSE_COOKIES.items()]

app = Application()


# json


@app.router.get("/async-plaintext-100B")
async def async_plaintext_100b(request: Request) -> Response:
    return text(test_data.TEXT_100B)


@app.router.get("/async-plaintext-1K")
async def async_plaintext_1k(request: Request) -> Response:
    return text(test_data.TEXT_1K)


@app.router.get("/async-plaintext-10K")
async def async_plaintext_10k(request: Request) -> Response:
    return text(test_data.TEXT_10K)


@app.router.get("/async-plaintext-100K")
async def async_plaintext_100k(request: Request) -> Response:
    return text(test_data.TEXT_100K)


@app.router.get("/async-plaintext-500K")
async def async_plaintext_500k(request: Request) -> Response:
    return text(test_data.TEXT_500K)


@app.router.get("/async-plaintext-1M")
async def async_plaintext_1m(request: Request) -> Response:
    return text(test_data.TEXT_1M)


@app.router.get("/async-plaintext-5M")
async def async_plaintext_5m(request: Request) -> Response:
    return text(test_data.TEXT_5M)


# plaintext sync


@app.router.get("/sync-plaintext-100B")
def sync_plaintext_100b(request: Request) -> Response:
    return text(test_data.TEXT_100B)


@app.router.get("/sync-plaintext-1K")
def sync_plaintext_1k(request: Request) -> Response:
    return text(test_data.TEXT_1K)


@app.router.get("/sync-plaintext-10K")
def sync_plaintext_10k(request: Request) -> Response:
    return text(test_data.TEXT_10K)


@app.router.get("/sync-plaintext-100K")
def sync_plaintext_100k(request: Request) -> Response:
    return text(test_data.TEXT_100K)


@app.router.get("/sync-plaintext-500K")
def sync_plaintext_500k(request: Request) -> Response:
    return text(test_data.TEXT_500K)


@app.router.get("/sync-plaintext-1M")
def sync_plaintext_1m(request: Request) -> Response:
    return text(test_data.TEXT_1M)


@app.router.get("/sync-plaintext-5M")
def sync_plaintext_5m(request: Request) -> Response:
    return text(test_data.TEXT_5M)


# JSON response


@app.router.get("/async-json-1K")
async def async_json_1k(request: Request) -> Response:
    return json(test_data.JSON_1K)


@app.router.get("/async-json-10K")
async def async_json_10k(request: Request) -> Response:
    return json(test_data.JSON_10K)


@app.router.get("/async-json-100K")
async def async_json_100k(request: Request) -> Response:
    return json(test_data.JSON_100K)


@app.router.get("/async-json-500K")
async def async_json_500k(request: Request) -> Response:
    return json(test_data.JSON_500K)


@app.router.get("/async-json-1M")
async def async_json_1m(request: Request) -> Response:
    return json(test_data.JSON_1M)


@app.router.get("/async-json-5M")
async def async_json_5m(request: Request) -> Response:
    return json(test_data.JSON_5M)


# JSON sync


@app.router.get("/sync-json-1K")
def sync_json_1k(request: Request) -> Response:
    return json(test_data.JSON_1K)


@app.router.get("/sync-json-10K")
def sync_json_10k(request: Request) -> Response:
    return json(test_data.JSON_10K)


@app.router.get("/sync-json-100K")
def sync_json_100k(request: Request) -> Response:
    return json(test_data.JSON_100K)


@app.router.get("/sync-json-500K")
def sync_json_500k(request: Request) -> Response:
    return json(test_data.JSON_500K)


@app.router.get("/sync-json-1M")
def sync_json_1m(request: Request) -> Response:
    return json(test_data.JSON_1M)


@app.router.get("/sync-json-5M")
def sync_json_5m(request: Request) -> Response:
    return json(test_data.JSON_5M)


# params


@app.router.get("/async-no-params")
async def async_no_params() -> Response:
    return no_content()


@app.router.get("/sync-no-params")
def sync_no_params() -> Response:
    return no_content()


@app.router.get("/async-path-params/{first}")
async def async_path_params(first: int) -> Response:
    return no_content()


@app.router.get("/sync-path-params/{first}")
def sync_path_params(first: int) -> Response:
    return no_content()


@app.router.get("/async-query-param")
async def async_query_params(request: Request) -> Response:
    int(request.query.get("first")[0])
    return no_content()


@app.router.get("/sync-query-param")
def sync_query_params(request: Request) -> Response:
    int(request.query.get("first")[0])
    return no_content()


@app.router.get("/async-mixed-params/{second}")
async def async_mixed_params(request: Request, second: int) -> Response:
    int(request.query.get("first")[0])
    return no_content()


@app.router.get("/sync-mixed-params/{second}")
def sync_mixed_params(request: Request, second: int) -> Response:
    int(request.query.get("first")[0])
    return no_content()


# headers
@app.router.get("/async-response-headers")
async def async_response_headers() -> Response:
    res = no_content()
    res.headers.update({k.encode("latin-1"): v.encode("latin-1") for k, v in test_data.RESPONSE_HEADERS.items()})
    return res


@app.router.get("/sync-response-headers")
def sync_response_headers() -> Response:
    res = no_content()
    res.headers.update({k.encode("latin-1"): v.encode("latin-1") for k, v in test_data.RESPONSE_HEADERS.items()})
    return res


# cookies
@app.router.get("/async-response-cookies")
async def async_response_cookies() -> Response:
    res = no_content()
    res.set_cookies(RESPONSE_COOKIES)
    return res


@app.router.get("/sync-response-cookies")
def sync_response_cookies() -> Response:
    res = no_content()
    res.set_cookies(RESPONSE_COOKIES)
    return res


# files async


@app.router.get("/async-file-response-100B")
async def async_file_response_100b() -> Response:
    content = await anyio.Path(test_data.FILE_100B).read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/async-file-response-1K")
async def async_file_response_1k() -> Response:
    content = await anyio.Path(test_data.FILE_1K).read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/async-file-response-10K")
async def async_file_response_10k() -> Response:
    content = await anyio.Path(test_data.FILE_10K).read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/async-file-response-100K")
async def async_file_response_100k() -> Response:
    content = await anyio.Path(test_data.FILE_100K).read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/async-file-response-500K")
async def async_file_response_500k() -> Response:
    content = await anyio.Path(test_data.FILE_500K).read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/async-file-response-1M")
async def async_file_response_1m() -> Response:
    content = await anyio.Path(test_data.FILE_1M).read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/async-file-response-5M")
async def async_file_response_5m() -> Response:
    content = await anyio.Path(test_data.FILE_5M).read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


# files sync


@app.router.get("/sync-file-response-100B")
def sync_file_response_100b() -> Response:
    content = test_data.FILE_100B.read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/sync-file-response-1K")
def sync_file_response_1k() -> Response:
    content = test_data.FILE_1K.read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/sync-file-response-10K")
def sync_file_response_10k() -> Response:
    content = test_data.FILE_10K.read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/sync-file-response-100K")
def sync_file_response_100k() -> Response:
    content = test_data.FILE_100K.read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/sync-file-response-500K")
def sync_file_response_500k() -> Response:
    content = test_data.FILE_500K.read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/sync-file-response-1M")
def sync_file_response_1m() -> Response:
    content = test_data.FILE_1M.read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


@app.router.get("/sync-file-response-5M")
def sync_file_response_5m() -> Response:
    content = test_data.FILE_5M.read_bytes()
    return file(content, file_name="response_file", content_type="application/octet-stream")


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


app.services.add_exact_scoped(SyncDependencyOne)
app.services.add_exact_scoped(SyncDependencyTwo)
app.services.add_exact_scoped(SyncDependencyThree)


@app.router.get("/sync-dependencies-sync")
def sync_dependencies_sync(
    injected_sync_one: SyncDependencyOne,
    injected_sync_two: SyncDependencyTwo,
    injected_sync_three: SyncDependencyThree,
) -> Response:
    return json(injected_sync_three.value)


@app.router.get("/async-dependencies-sync")
async def async_dependencies_sync(
    injected_sync_one: SyncDependencyOne,
    injected_sync_two: SyncDependencyTwo,
    injected_sync_three: SyncDependencyThree,
) -> Response:
    return json(injected_sync_three.value)


# request body json


@app.router.post("/async-post-json")
async def async_post_json(request: Request) -> Response:
    data = await request.json()
    return no_content()


# request body multipart


@app.router.post("/async-post-multipart-form")
async def async_post_multipart_form(request: Request, data: FromForm) -> Response:
    return no_content()


@app.router.post("/sync-post-multipart-form")
def sync_post_multipart_form(request: Request, data: FromForm) -> Response:
    return no_content()
