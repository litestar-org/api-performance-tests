from blacksheep import Application, text

app = Application()


@app.router.get("/async-plaintext-no-params")
async def async_plaintext_no_params() -> text:
    return text("Hello, world!")


@app.router.get("/sync-plaintext-no-params")
def sync_plaintext_no_params() -> text:
    return text("Hello, world!")


@app.router.get("/async-plaintext/{first}")
async def async_plaintext_path_param(first: int) -> text:
    return text(f"The number is {first * 2}")


@app.router.get("/sync-plaintext/{first}")
def sync_plaintext_path_param(first: int) -> text:
    return text(f"The number is {first * 2}")


@app.router.get("/async-plaintext-query-param")
async def async_plaintext_query_param(first: int) -> text:
    return text(f"The number is {first * 2}")


@app.router.get("/sync-plaintext-query-param")
def sync_plaintext_query_param(first: int) -> text:
    return text(f"The number is {first * 2}")


@app.router.get("/async-plaintext-mixed-params/{second}")
async def async_plaintext_mixed_params(first: int, second: int) -> text:
    return text(f"The number is {first + second}")


@app.router.get("/sync-plaintext-mixed-params/{second}")
def sync_plaintext_mixed_params(first: int, second: int) -> text:
    return text(f"The number is {first + second}")
