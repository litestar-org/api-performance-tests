from asyncio import sleep

from starlite import MediaType, Starlite, get


@get(path="/json-async")
async def json_async() -> dict[str, str]:
    await sleep(0.0001)
    return {"message": "Hello, world!"}


@get(path="/json-sync")
def json_sync() -> dict[str, str]:
    return {"message": "Hello, world!"}


@get(path="/{path_param:int}", media_type=MediaType.TEXT)
def path_param(path_param: int) -> str:
    return str(path_param)


@get(path="/query-param", media_type=MediaType.TEXT)
def query_param(value: int) -> str:
    return str(value)


app = Starlite(
    route_handlers=[
        json_async,
        json_sync,
        path_param,
        query_param,
    ],
    openapi_config=None,
)
