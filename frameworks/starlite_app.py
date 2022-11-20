from starlite import MediaType, Starlite, get


@get("/async-plaintext-no-params", media_type=MediaType.TEXT)
async def async_plaintext_no_params() -> str:
    return "Hello, world!"


@get("/sync-plaintext-no-params", media_type=MediaType.TEXT)
def sync_plaintext_no_params() -> str:
    return "Hello, world!"


@get("/async-plaintext/{first:int}", media_type=MediaType.TEXT)
async def async_plaintext_path_param(first: int) -> str:
    return f"The number is {first * 2}"


@get("/sync-plaintext/{first:int}", media_type=MediaType.TEXT)
def sync_plaintext_path_param(first: int) -> str:
    return f"The number is {first * 2}"


@get("/async-plaintext-query-param", media_type=MediaType.TEXT)
async def async_plaintext_query_param(first: int) -> str:
    return f"The number is {first * 2}"


@get("/sync-plaintext-query-param", media_type=MediaType.TEXT)
def sync_plaintext_query_param(first: int) -> str:
    return f"The number is {first * 2}"


@get("/async-plaintext-mixed-params/{second:int}", media_type=MediaType.TEXT)
async def async_plaintext_mixed_params(first: int, second: int) -> str:
    return f"The number is {first + second}"


@get("/sync-plaintext-mixed-params/{second:int}", media_type=MediaType.TEXT)
def sync_plaintext_mixed_params(first: int, second: int) -> str:
    return f"The number is {first + second}"


app = Starlite(
    route_handlers=[
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
