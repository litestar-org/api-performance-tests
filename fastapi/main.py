from asyncio import sleep

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()


@app.get("/json-async")
async def json_async() -> ORJSONResponse:
    await sleep(0.0001)
    return ORJSONResponse({"message": "Hello, world!"})


@app.get("/json-sync")
def json_sync() -> ORJSONResponse:
    return ORJSONResponse({"message": "Hello, world!"})


@app.get("/{path_param:int}")
def path_param(path_param: int) -> str:
    return str(path_param)


@app.get("/query-param")
def query_param(value: int) -> str:
    return str(value)
