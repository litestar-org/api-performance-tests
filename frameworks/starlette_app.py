from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse

app = Starlette()


@app.route(path="/async-plaintext-no-params", methods=["GET"])
async def async_plaintext_no_params(_) -> PlainTextResponse:
    return PlainTextResponse("Hello, world!")


@app.route(path="/sync-plaintext-no-params", methods=["GET"])
def sync_plaintext_no_params(_) -> PlainTextResponse:
    return PlainTextResponse("Hello, world!")


@app.route(path="/async-plaintext/{first:int}", methods=["GET"])
async def async_plaintext_path_param(request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"The number is {request.path_params['first'] * 2}")


@app.route(path="/sync-plaintext/{first:int}", methods=["GET"])
def sync_plaintext_path_param(request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"The number is {request.path_params['first'] * 2}")


@app.route(path="/async-plaintext-query-param", methods=["GET"])
async def async_plaintext_query_param(request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"The number is {int(request.query_params['first']) * 2}")


@app.route(path="/sync-plaintext-query-param", methods=["GET"])
def sync_plaintext_query_param(request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"The number is {int(request.query_params['first']) * 2}")


@app.route(path="/async-plaintext-mixed-params/{second:int}", methods=["GET"])
async def async_plaintext_mixed_params(request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"The number is {int(request.query_params['first']) + request.path_params['second']}")


@app.route(path="/sync-plaintext-mixed-params/{second:int}", methods=["GET"])
def sync_plaintext_mixed_params(request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"The number is {int(request.query_params['first']) + request.path_params['second']}")
