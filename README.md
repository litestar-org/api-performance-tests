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


## Executing the Tests

To execute the tests:

1. clone the repo
2. build the docker image with `./build.sh`
3. run the desired benchmarks with `./run.sh`

### Benchmarks
#### Comparing against other frameworks

- `./run.sh bench-frameworks -f all` will run tests comparing Starlite, Starlette, Sanic, FastAPI and blacksheep
- `./run.sh bench-frameworks -f starlite -f sanic` will run tests comparing Starlite and Sanic

#### Comparing different Starlite versions

`./run.sh bench-branches v1.20.0 v1.39.0 performance_updates` will run tests comparing Starlite releases `v1.20.0`, `v1.39.0`
and the `performance_updates` branch

#### Settings

|                                     |                                                      |
|-------------------------------------|------------------------------------------------------|
| -d, --duration                      | duration of the test          (default: 15s)         |
| -w, --warmup                        | duration of the warmup period (default: 5s)          |
| -e, --endpoints [sync&#124;async]   | endpoint types to select      (default: sync, async) |
| -m, --mode      [load&#124;latency] | benchmarking mode (sustained load or burst latency)  |


### Analyzing the results

- `./run.sh analyze` will create plots of the test results and store them in the `results` folder
- `./run.sh analyze -p 75` will create plots of the test results using measurements in the 75th percentile
and store them in the `results` folder

#### Running the analysis locally

The above commands run the analysis within the docker image. This is not necessary, and you can set up your environment
to run it locally as well:

- Install dependencies with `poetry install`
- Run analysis with `python cli.py analysis`


## Updating Dependencies

To update the dependencies simply run `poetry update` and `pnpm up` respectively. These commands are executed as part
of the test script, ensuring dependencies are always up to date.

## Contributing

PRs are welcome.

Please make sure to install [pre-commit](https://pre-commit.com/) on your system, and then execute `pre-commit install`
in the repository root - this will ensure the pre-commit hooks are in place.

After doing this, add a PR with your changes and a clear description of the changes.
