from sanic import Sanic
from sanic.response import text

app = Sanic("MyApp")


@app.get("/async-plaintext-no-params")
async def async_plaintext_no_params(_) -> text:
    return text("Hello, world!")


@app.get("/sync-plaintext-no-params")
def sync_plaintext_no_params(_) -> text:
    return text("Hello, world!")


@app.get("/async-plaintext/<first:int>")
async def async_plaintext_path_param(_, first: int) -> text:
    return text(f"The number is {first * 2}")


@app.get("/sync-plaintext/<first:int>")
def sync_plaintext_path_param(_, first: int) -> text:
    return text(f"The number is {first * 2}")


@app.get("/async-plaintext-query-param")
async def async_plaintext_query_param(request) -> text:
    return text(f"The number is {int(request.args.get('first')) * 2}")


@app.get("/sync-plaintext-query-param")
def sync_plaintext_query_param(request) -> text:
    return text(f"The number is {int(request.args.get('first')) * 2}")


@app.get("/async-plaintext-mixed-params/<second:int>")
async def async_plaintext_mixed_params(request, second: int) -> text:
    return text(f"The number is {int(request.args.get('first')) + second}")


@app.get("/sync-plaintext-mixed-params/<second:int>")
def sync_plaintext_mixed_params(request, second: int) -> text:
    return text(f"The number is {int(request.args.get('first')) + second}")
