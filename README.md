# api-performance-tests

This is an API performance test comparing Starlite and FastAPI using autocannon.

Setup is identical for both frameworks -

1. a sync endpoint returning JSON
2. a async endpoint returning JSON
3. a plaintext endpoint receiving a path parameter
4. a plaintext endpoint receiving a query parameter

All frameworks use orjson for serialization of the responses and identical uvicorn + gunicorn settings (max workers).
This is meant to ensure that the serialization speed of orjson is not considered in the benchmarks.
It should be noted though that only `starlite` uses orjson by default.

Autocannon settings: 4 repetitions for each endpoint, using 4 workers and 30 connections for 10 seconds.

Last run results:

![Result](result.png)

You can view the result json files under `/results`

The plotting is done using pandas - script is under `/analysis`

## Executing Tests Locally

To execute the tests:

1. clone the repo
2. run ./test.sh

The test.sh script will install the dependencies for you.

note: the repository is setup to use python 3.10+

## Contributing

Please make sure to install [pre-commit](https://pre-commit.com/) on your system, and then execute `pre-commit install` in the repository root - this will ensure the pre-commit hooks are in place.

After doing this, add a PR with your changes and a clear description of the change.
