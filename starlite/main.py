from asyncio import sleep

from starlite import MediaType, Starlite, get

# json


@get("/async-json-no-params", media_type=MediaType.JSON)
async def async_json_no_params() -> dict:
    await sleep(0.0000000001)
    return {"message": "Hello, world!"}


@get("/sync-json-no-params", media_type=MediaType.JSON)
def sync_json_no_params() -> dict:
    return {"message": "Hello, world!"}


@get("/async-json/{first:str}", media_type=MediaType.JSON)
async def async_json_path_param(first: str) -> dict:
    await sleep(0.0000000001)
    return {"message": first}


@get("/sync-json/{first:str}", media_type=MediaType.JSON)
def sync_json_path_param(first: str) -> dict:
    return {"message": first}


@get("/async-json-query-param", media_type=MediaType.JSON)
async def async_json_query_param(first: str) -> dict:
    await sleep(0.0000000001)
    return {"message": first}


@get("/sync-json-query-param", media_type=MediaType.JSON)
def sync_json_query_param(first: str) -> dict:
    return {"message": first}


@get("/async-json-mixed-params/{second:str}", media_type=MediaType.JSON)
async def async_json_mixed_params(first: str, second: str) -> dict:
    await sleep(0.0000000001)
    return {"message": first + second}


@get("/sync-json-mixed-params/{second:str}", media_type=MediaType.JSON)
def sync_json_mixed_params(first: str, second: str) -> dict:
    return {"message": first + second}


# plain text


@get("/async-plaintext-no-params", media_type=MediaType.TEXT)
async def async_plaintext_no_params() -> str:
    await sleep(0.0000000001)
    return "Hello, world!"


@get("/sync-plaintext-no-params", media_type=MediaType.TEXT)
def sync_plaintext_no_params() -> str:
    return "Hello, world!"


@get("/async-plaintext/{first:str}", media_type=MediaType.TEXT)
async def async_plaintext_path_param(first: str) -> str:
    await sleep(0.0000000001)
    return first


@get("/sync-plaintext/{first:str}", media_type=MediaType.TEXT)
def sync_plaintext_path_param(first: str) -> str:
    return first


@get("/async-plaintext-query-param", media_type=MediaType.TEXT)
async def async_plaintext_query_param(first: str) -> str:
    await sleep(0.0000000001)
    return first


@get("/sync-plaintext-query-param", media_type=MediaType.TEXT)
def sync_plaintext_query_param(first: str) -> str:
    return first


@get("/async-plaintext-mixed-params/{second:str}", media_type=MediaType.TEXT)
async def async_plaintext_mixed_params(first: str, second: str) -> str:
    await sleep(0.0000000001)
    return first + second


@get("/sync-plaintext-mixed-params/{second:str}", media_type=MediaType.TEXT)
def sync_plaintext_mixed_params(first: str, second: str) -> str:
    return first + second


app = Starlite(
    route_handlers=[
        async_json_no_params,
        sync_json_no_params,
        async_json_path_param,
        sync_json_path_param,
        async_json_query_param,
        sync_json_query_param,
        async_json_mixed_params,
        sync_json_mixed_params,
        async_plaintext_no_params,
        sync_plaintext_no_params,
        async_plaintext_path_param,
        sync_plaintext_path_param,
        async_plaintext_query_param,
        sync_plaintext_query_param,
        async_plaintext_mixed_params,
        sync_plaintext_mixed_params,
    ],
    openapi_config=None,
)
