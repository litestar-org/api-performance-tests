import math

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, PlainTextResponse

app = FastAPI()


def calculate_square() -> dict:
    result = {}
    i = 1
    while i < 1000:
        result[str(i)] = str(math.pow(i, 2))
        i += 1
    return result


@app.get("/square-sync")
def calculate_square_sync():
    return ORJSONResponse(content={"data": calculate_square()})


@app.get("/square-async")
async def calculate_square_async():
    return ORJSONResponse(content={"data": calculate_square()})


@app.get("/json")
async def json_serialization():
    return ORJSONResponse({"message": "Hello, world!"})


@app.get("/plaintext")
async def plaintext():
    return PlainTextResponse(b"Hello, world!")
