# api-performance-tests

This is an API performance test comparing:

1. [Starlite](https://github.com/starlite-api/starlite)
2. [Starlette](https://github.com/encode/starlette)
3. [FastAPI](https://github.com/tiangolo/fastapi)
4. [Sanic](https://github.com/sanic-org/sanic)
5. [BlackSheep](https://github.com/Neoteroi/BlackSheep)

Using the [autocannon](https://github.com/mcollina/autocannon) stress testing tool.

## Last Run Results

![Plain Text Results](result.png)

You can view the last run results under the `/results` folder - it contains json files with the output.
The plotting is done using pandas - script is under `/analysis`.

Note: PRs improving the analysis script are welcome.

## Test Setup

Setup is identical for all frameworks.

- The applications are in the folders with their names - `/starlite`, `/starlette`, `/fastapi`, `/scanic`, `/blacksheep`.
- There are no DB querying tests because all frameworks are DB agnostic and as such this has no value in itself.
- All frameworks are testing using plaintext responses, thus not factoring in any 3rd party json libraries etc.

### Endpoints

1. sync endpoint without query or path parameters returning text (s-np)
2. async endpoint without query or path parameters returning text (a-np)
3. sync endpoint with a query parameter returning text (s-qp)
4. async endpoint with a query parameter returning text (a-qp)
5. sync endpoint with a path parameter returning text (s-pp)
6. async endpoint with a path parameter returning text (a-pp)
7. sync endpoint with mixed parameters returning text (s-mp)
8. async endpoint with mixed parameters returning text (a-mp)

#### Autocannon Settings:

Each endpoint for each framework is stress using the `autocannon` default settings x2 times.

#### Uvicorn/Gunicorn Settings:

The applications are launched using gunicorn with uvicorn workers - their number depends on the available threads in the
machine. The settings are identical for all applications, you can see it in the `gunicorn.config.py` in each application
folder.

## Executing the Tests

To execute the tests:

1. clone the repo
2. run `./test.sh`

The test.sh script will create a virtual environment and install the dependencies for you using poetry.

### Notes:

- the script requires python 3.11, node 18+ and curl to be installed on the system.
- if poetry is not installed on your system, it will be installed by the script.
- if pnpm is not installed on your system, it will be installed by the script.

## Updating Dependencies

To update the dependencies simply run `poetry update` and `pnpm up` respectively. These commands are executed as part
of the test script, ensuring dependencies are always up to date.

## Contributing

PRs are welcome.

Please make sure to install [pre-commit](https://pre-commit.com/) on your system, and then execute `pre-commit install`
in the repository root - this will ensure the pre-commit hooks are in place.

After doing this, add a PR with your changes and a clear description of the changes.
