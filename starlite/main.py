import math

from starlite import MediaType, Starlite, get


def calculate_square() -> dict:
    result = {}
    i = 1
    while i < 1000:
        result[str(i)] = str(math.pow(i, 2))
        i += 1
    return result


@get("/square-sync")
def calculate_square_sync() -> dict[str, str]:
    return {"data": calculate_square()}


@get("/square-async")
async def calculate_square_async() -> dict[str, str]:
    return {"data": calculate_square()}


@get(path="/json")
def json_serialization() -> dict[str, str]:
    return {"message": "Hello, world!"}


@get(path="/plaintext", media_type=MediaType.TEXT)
def plaintext() -> bytes:
    return b"Hello, world!"


app = Starlite(
    route_handlers=[
        calculate_square_sync,
        calculate_square_async,
        json_serialization,
        plaintext,
    ],
)
