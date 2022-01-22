# api-performance-tests

This is an API performance test comparing Starlite and FastAPI using autocannon.

Setup is identical for both frameworks -

1. a sync endpoint returing a json object with some square root calculations
2. a async endpoint returing a json object with some square root calculations
3. a json endpoint returning {"hello": "world"}
4. a plaintext endpoint returning "hello world"

Both frameworks use orjson for serialization of the responses and identical uvicorn + gunicorn settings (max workers)

Autocannon settings: 4 repetitions for each endpoint, using 4 workers and 25 connections for 10 seconds.

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
