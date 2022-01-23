from asyncio import sleep
from typing import Any

import orjson

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

app = Starlette()


class ORJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


@app.route(path="/json-async", methods=["GET"])
async def json_async(_) -> ORJSONResponse:
    await sleep(0.0001)
    return ORJSONResponse({"message": "Hello, world!"})


@app.route(path="/json-sync", methods=["GET"])
def json_sync(_) -> ORJSONResponse:
    return ORJSONResponse({"message": "Hello, world!"})


@app.route(path="/{path_param:int}", methods=["GET"])
def path_param(request: Request) -> str:
    return PlainTextResponse(str(request.path_params["path_param"]))


@app.route(path="/query-param", methods=["GET"])
def query_param(request: Request) -> str:
    return PlainTextResponse(str(request.query_params["value"]))
