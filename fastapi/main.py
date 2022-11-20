from asyncio import sleep

from fastapi import FastAPI

app = FastAPI()


@app.get("/async-plaintext-no-params")
async def async_plaintext_no_params() -> str:
    await sleep(0.0001)
    return "Hello, world!"


@app.get("/sync-plaintext-no-params")
def sync_plaintext_no_params() -> str:
    return "Hello, world!"


@app.get("/async-plaintext/{first:int}")
async def async_plaintext_path_param(first: int) -> str:
    await sleep(0.0001)
    return f"The number is {first * 2}"


@app.get("/sync-plaintext/{first:int}")
def sync_plaintext_path_param(first: int) -> str:
    return f"The number is {first * 2}"


@app.get("/async-plaintext-query-param")
async def async_plaintext_query_param(first: int) -> str:
    await sleep(0.0001)
    return f"The number is {first * 2}"


@app.get("/sync-plaintext-query-param")
def sync_plaintext_query_param(first: int) -> str:
    return f"The number is {first * 2}"


@app.get("/async-plaintext-mixed-params/{second:int}")
async def async_plaintext_mixed_params(first: int, second: int) -> str:
    await sleep(0.0001)
    return f"The number is {first * second}"


@app.get("/sync-plaintext-mixed-params/{second:int}")
def sync_plaintext_mixed_params(first: int, second: int) -> str:
    return f"The number is {first * second}"
