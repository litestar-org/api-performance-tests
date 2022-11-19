from asyncio import sleep

from fastapi import FastAPI

app = FastAPI()


# json


@app.get("/async-json-no-params")
async def async_json_no_params() -> dict:
    await sleep(0)
    return {"message": "Hello, world!"}


@app.get("/sync-json-no-params")
def sync_json_no_params() -> dict:
    return {"message": "Hello, world!"}


@app.get("/async-json/{first:str}")
async def async_json_path_param(first: str) -> dict:
    await sleep(0)
    return {"message": first}


@app.get("/sync-json/{first:str}")
def sync_json_path_param(first: str) -> dict:
    return {"message": first}


@app.get("/async-json-query-param")
async def async_json_query_param(first: str) -> dict:
    await sleep(0)
    return {"message": first}


@app.get("/sync-json-query-param")
def sync_json_query_param(first: str) -> dict:
    return {"message": first}


@app.get("/async-json-mixed-params/{second:str}")
async def async_json_mixed_params(first: str, second: str) -> dict:
    await sleep(0)
    return {"message": first + second}


@app.get("/sync-json-mixed-params/{second:str}")
def sync_json_mixed_params(first: str, second: str) -> dict:
    return {"message": first + second}


# plain text


@app.get("/asleep(ASYNC_SLEEP)")
async def async_plaintext_no_params() -> str:
    await sleep(0)
    return "Hello, world!"


@app.get("/sleep(ASYNC_SLEEP)")
def sync_plaintext_no_params() -> str:
    return "Hello, world!"


@app.get("/async-plaintext/{first:str}")
async def async_plaintext_path_param(first: str) -> str:
    await sleep(0)
    return first


@app.get("/sync-plaintext/{first:str}")
def sync_plaintext_path_param(first: str) -> str:
    return first


@app.get("/async-plaintext-query-param")
async def async_plaintext_query_param(first: str) -> str:
    return first


@app.get("/sync-plaintext-query-param")
def sync_plaintext_query_param(first: str) -> str:
    return first


@app.get("/async-plaintext-mixed-params/{second:str}")
async def async_plaintext_mixed_params(first: str, second: str) -> str:
    return first + second


@app.get("/sync-plaintext-mixed-params/{second:str}")
def sync_plaintext_mixed_params(first: str, second: str) -> str:
    return first + second
