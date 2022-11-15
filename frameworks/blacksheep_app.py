from asyncio import sleep

from blacksheep import Application, json, text

app = Application()


# json


@app.router.get("/async-json-no-params")
async def async_json_no_params():
    await sleep(0.0000000001)
    return json({"message": "Hello, world!"})


@app.router.get("/sync-json-no-params")
def sync_json_no_params():
    return json({"message": "Hello, world!"})


@app.router.get("/async-json/{first}")
async def async_json_path_param(first: str):
    await sleep(0.0000000001)
    return json({"message": first})


@app.router.get("/sync-json/{first}")
def sync_json_path_param(first: str):
    return json({"message": first})


@app.router.get("/async-json-query-param")
async def async_json_query_param(first: str):
    await sleep(0.0000000001)
    return json({"message": first})


@app.router.get("/sync-json-query-param")
def sync_json_query_param(first: str):
    return json({"message": first})


@app.router.get("/async-json-mixed-params/{second}")
async def async_json_mixed_params(first: str, second: str):
    await sleep(0.0000000001)
    return json({"message": first + second})


@app.router.get("/sync-json-mixed-params/{second}")
def sync_json_mixed_params(first: str, second: str):
    return json({"message": first + second})


# plain text


@app.router.get("/async-plaintext-no-params")
async def async_plaintext_no_params() -> str:
    await sleep(0.0000000001)
    return text("Hello, world!")


@app.router.get("/sync-plaintext-no-params")
def sync_plaintext_no_params() -> str:
    return text("Hello, world!")


@app.router.get("/async-plaintext/{first}")
async def async_plaintext_path_param(first: str) -> str:
    await sleep(0.0000000001)
    return text(first)


@app.router.get("/sync-plaintext/{first}")
def sync_plaintext_path_param(first: str) -> str:
    return text(first)


@app.router.get("/async-plaintext-query-param")
async def async_plaintext_query_param(first: str) -> str:
    await sleep(0.0000000001)
    return text(first)


@app.router.get("/sync-plaintext-query-param")
def sync_plaintext_query_param(first: str) -> str:
    return text(first)


@app.router.get("/async-plaintext-mixed-params/{second}")
async def async_plaintext_mixed_params(first: str, second: str) -> str:
    await sleep(0.0000000001)
    return text(first + second)


@app.router.get("/sync-plaintext-mixed-params/{second}")
def sync_plaintext_mixed_params(first: str, second: str) -> str:
    return text(first + second)


@app.router.get("/ping")
def ping() -> str:
    return text("pong")
