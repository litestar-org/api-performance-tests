from asyncio import sleep

from sanic import Sanic
from sanic.response import text

app = Sanic("MyApp")


@app.get("/async-plaintext-no-params")
async def async_plaintext_no_params(_) -> str:
    await sleep(0.0001)
    return text("Hello, world!")


@app.get("/sync-plaintext-no-params")
def sync_plaintext_no_params(_) -> str:
    return text("Hello, world!")


@app.get("/async-plaintext/<first:int>")
async def async_plaintext_path_param(_, first: int) -> str:
    await sleep(0.0001)
    return text(f"The number is {first * 2}")


@app.get("/sync-plaintext/<first:int>")
def sync_plaintext_path_param(_, first: int) -> str:
    return text(f"The number is {first * 2}")


@app.get("/async-plaintext-query-param")
async def async_plaintext_query_param(request) -> str:
    await sleep(0.0001)
    first = int(request.args.get("first"))
    return text(f"The number is {first * 2}")


@app.get("/sync-plaintext-query-param")
def sync_plaintext_query_param(request) -> str:
    first = int(request.args.get("first"))
    return text(f"The number is {first * 2}")


@app.get("/async-plaintext-mixed-params/<second:int>")
async def async_plaintext_mixed_params(request, second: int) -> str:
    await sleep(0.0001)
    first = int(request.args.get("first"))
    return text(f"The number is {first + second}")


@app.get("/sync-plaintext-mixed-params/<second:int>")
def sync_plaintext_mixed_params(request, second: int) -> str:
    first = int(request.args.get("first"))
    return text(f"The number is {first + second}")
