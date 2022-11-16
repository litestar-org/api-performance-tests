from asyncio import sleep

from orjson import dumps
from sanic import Sanic
from sanic.response import json, text

app = Sanic("MyApp")

# json


@app.get("/async-json-no-params")
async def async_json_no_params(_) -> dict:
    await sleep(0)
    return json({"message": "Hello, world!"}, dumps=dumps)


@app.get("/sync-json-no-params")
def sync_json_no_params(_) -> dict:
    return json({"message": "Hello, world!"}, dumps=dumps)


@app.get("/async-json/<first:str>")
async def async_json_path_param(_, first: str) -> dict:
    await sleep(0)
    return json({"message": first}, dumps=dumps)


@app.get("/sync-json/<first:str>")
def sync_json_path_param(_, first: str) -> dict:
    return json({"message": first}, dumps=dumps)


@app.get("/async-json-query-param")
async def async_json_query_param(request) -> dict:
    await sleep(0)
    return json({"message": request.args.get("first")}, dumps=dumps)


@app.get("/sync-json-query-param")
def sync_json_query_param(request) -> dict:
    return json({"message": request.args.get("first")}, dumps=dumps)


@app.get("/async-json-mixed-params/<second:str>")
async def async_json_mixed_params(request, second: str) -> dict:
    await sleep(0)
    return json({"message": request.args.get("first") + second}, dumps=dumps)


@app.get("/sync-json-mixed-params/<second:str>")
def sync_json_mixed_params(request, second: str) -> dict:
    return json({"message": request.args.get("first") + second}, dumps=dumps)


# plain text


@app.get("/async-plaintext-no-params")
async def async_plaintext_no_params(_) -> str:
    await sleep(0)
    return text("Hello, world!")


@app.get("/sync-plaintext-no-params")
def sync_plaintext_no_params(_) -> str:
    return text("Hello, world!")


@app.get("/async-plaintext/<first:str>")
async def async_plaintext_path_param(_, first: str) -> str:
    await sleep(0)
    return text(first)


@app.get("/sync-plaintext/<first:str>")
def sync_plaintext_path_param(_, first: str) -> str:
    return text(first)


@app.get("/async-plaintext-query-param")
async def async_plaintext_query_param(request) -> str:
    await sleep(0)
    return text(request.args.get("first"))


@app.get("/sync-plaintext-query-param")
def sync_plaintext_query_param(request) -> str:
    return text(request.args.get("first"))


@app.get("/async-plaintext-mixed-params/<second:str>")
async def async_plaintext_mixed_params(request, second: str) -> str:
    await sleep(0)
    return text(request.args.get("first") + second)


@app.get("/sync-plaintext-mixed-params/<second:str>")
def sync_plaintext_mixed_params(request, second: str) -> str:
    return text(request.args.get("first") + second)
