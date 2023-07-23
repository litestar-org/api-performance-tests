<!-- markdownlint-disable -->
<p align="center">
  <img src="https://github.com/litestar-org/branding/blob/473f54621e55cde9acbb6fcab7fc03036173eb3d/assets/Branding%20-%20SVG%20-%20Transparent/Logo%20-%20Banner%20-%20Inline%20-%20Light.svg#gh-light-mode-only" alt="Litestar Logo - Light" width="100%" height="auto" />
  <img src="https://github.com/litestar-org/branding/blob/473f54621e55cde9acbb6fcab7fc03036173eb3d/assets/Branding%20-%20SVG%20-%20Transparent/Logo%20-%20Banner%20-%20Inline%20-%20Dark.svg#gh-dark-mode-only" alt="Litestar Logo - Dark" width="100%" height="auto" />
</p>
<!-- markdownlint-restore -->

<div align="center">

<!-- prettier-ignore-start -->

| Project   |     | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-----------|:----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Community |     | [![Reddit](https://img.shields.io/reddit/subreddit-subscribers/litestarapi?label=r%2FLitestar&logo=reddit&labelColor=202235&color=edb641&logoColor=edb641)](https://reddit.com/r/litestarapi) [![Discord](https://img.shields.io/discord/919193495116337154?labelColor=202235&color=edb641&label=chat%20on%20discord&logo=discord&logoColor=edb641)](https://discord.gg/X3FJqy8d2j) [![Matrix](https://img.shields.io/badge/chat%20on%20Matrix-bridged-202235?labelColor=202235&color=edb641&logo=matrix&logoColor=edb641)](https://matrix.to/#/#litestar:matrix.org) [![Medium](https://img.shields.io/badge/Medium-202235?labelColor=202235&color=edb641&logo=medium&logoColor=edb641)](https://blog.litestar.dev) [![Twitter](https://img.shields.io/twitter/follow/LitestarAPI?labelColor=202235&color=edb641&logo=twitter&logoColor=edb641&style=flat)](https://twitter.com/LitestarAPI) [![Blog](https://img.shields.io/badge/Blog-litestar.dev-202235?logo=blogger&labelColor=202235&color=edb641&logoColor=edb641)](https://blog.litestar.dev) |
| Meta      |     | [![Litestar Project](https://img.shields.io/badge/Litestar%20Org-%E2%AD%90%20API%20Perf%20Tests-202235.svg?logo=python&labelColor=202235&color=edb641&logoColor=edb641)](https://github.com/litestar-org/litestar) [![License - MIT](https://img.shields.io/badge/license-MIT-202235.svg?logo=python&labelColor=202235&color=edb641&logoColor=edb641)](https://spdx.org/licenses/) [![Litestar Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-%23edb641.svg?&logo=github&logoColor=edb641&labelColor=202235)](https://github.com/sponsors/litestar-org) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json&labelColor=202235)](https://github.com/astral-sh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&labelColor=202235&logoColor=edb641)](https://github.com/psf/black)                                                                                                                        |

<!-- prettier-ignore-end -->
</div>

# api-performance-tests

> **Note**
> [**_Starlite has been renamed to Litestar_**](https://litestar.dev/about/organization.html#litestar-and-starlite)

This is an API performance test comparing:
1. [Litestar](https://github.com/litestar-org/litestar)
2. [Starlite v1.5x](https://github.com/litestar-org/litestar/tree/v1.51)
3. [Starlette](https://github.com/encode/starlette)
4. [FastAPI](https://github.com/tiangolo/fastapi)
5. [Sanic](https://github.com/sanic-org/sanic)
6. [BlackSheep](https://github.com/Neoteroi/BlackSheep)

Using the [bombardier](https://github.com/codesenberg/bombardier) HTTP benchmarking tool.

## Last Run Results

![Plain Text Results](result.png)

You can view the last run results under the `/results` folder - it contains json files with the output.
The plotting is done using pandas - script is under `/analysis`.

Note: PRs improving the analysis script are welcome.

## Test Setup

Setup is identical for all frameworks.

- Applications reside in the `frameworks` folder and consist of a single file named `<framework_name>_app.py`

### Tests

All tests are run sync and async

#### Serialization and data sending

##### Plaintext

- Sending 100 bytes plaintext
- Sending 1kB plaintext
- Sending 10kB plaintext
- Sending 100kB plaintext
- Sending 500kB plaintext
- Sending 1MB plaintext
- Sending 5MB plaintext

##### JSON

Serializing a dictionary into JSON

- Serializing and sending 1kB JSON
- Serializing and sending 10kB JSON
- Serializing and sending 100kB JSON
- Serializing and sending 500kB JSON
- Serializing and sending 1MB JSON

##### Serialization

(only supported by `Litestar` and `FastAPI`)

- Serializing 50 dataclass objects each referencing 2 more dataclass objects
- Serializing 100 dataclass objects each referencing 5 more dataclass objects
- Serializing 500 dataclass objects each referencing 3 more dataclass objects
- Serializing 50 pydantic objects each referencing 2 more pydantic objects
- Serializing 100 pydantic objects each referencing 5 more pydantic objects
- Serializing 500 pydantic objects each referencing 3 more pydantic objects

##### Files

- Sending a 100 bytes binary file
- Sending a 1kB bytes binary file
- Sending a 50kB binary file
- Sending a 1MB bytes binary file

#### Path amd query parameter handling

All responses return "No Content"

- No path parameters
- Single path parameter, coerced into an integer
- Single query parameter, coerced into an integer
- A path and a query parameters, coerced into integers

#### Dependency injection

(not supported by `Starlette`)

- Resolving 3 nested synchronous dependencies
- Resolving 3 nested asynchronous dependencies (only supported by `Litestar` and `FastAPI`)
- Resolving 3 nested synchronous, and 3 nested asynchronous dependencies (only supported by `Litestar` and `FastAPI`)

#### Modifying responses

All responses return "No Content"

- Setting response headers
- Setting response cookies

## Running the tests

### Prerequisites

- [docker](https://docs.docker.com/get-docker/)
- [poetry](https://python-poetry.org/docs/#installation)
- Python 3.11

### Running tests

1. Clone this repo
2. Run `poetry install`
3. Run tests with `bench run --rps --latency`

After the run, the results will be stored in `results/run_<run_mumber>.json`

#### Selecting which frameworks to test

To select a framework, simply pass its name to the `run command`:

`bench run --rps litestar starlette fastapi`

##### Selecting a framework version

- A version available on PyPi: `bench run --rps litestar@v1.40.0`
- A version from git: `bench run --rps litestar@git+branch_or_tag_name`
- A version from a specific git repository: `bench run --rps litestar@git+https://github.com/litestar-org/litestar.git@branch_or_tag_name`
- A local file: `bench run --rps litestar@file+/path/to/litestar`

#### Running a specific test

You can run a single test by specifying its full name and category:

`bench run --rps litestar -t json:json-1K`

#### Test Settings

|                                                                                                                                                                       |                                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| -r, --rebuild                                                                                                                                                         | rebuild docker images                                           |
| -L, --latency                                                                                                                                                         | run latency tests                                               |
| -R, --rps                                                                                                                                                             | run RPS tests                                                   |
| -w, --warmup                                                                                                                                                          | duration of the warmup period (default: 5s)                     |
| -e, --endpoint mode [sync&#124;async]                                                                                                                                 | endpoint types to select (default: sync, async)                 |
| -c, --endpoint-category [plaintext&#124;json&#124;files&#124;params&#124;dynamic-response&#124;dependency-injection&#124;serialization&#124;post-json&#124;post-body] | test types to select (default: all)                             |
| -d, --duration                                                                                                                                                        | duration of the rps benchmarks (default: 15s)                   |
| -l, --limit                                                                                                                                                           | max requests per second for latency benchmarks (default: 20)    |
| -r, --requests                                                                                                                                                        | total number of requests for latency benchmarks (default: 1000) |

### Analyzing the results

- Run `bench results` to generate plots from the latest test results
- Run `bench results -s` to generate plots from the latest test results and split them into separate files for each category

## Contributing

PRs are welcome.

Please make sure to install [pre-commit](https://pre-commit.com/) on your system, and then execute `pre-commit install`
in the repository root - this will ensure the pre-commit hooks are in place.

After doing this, add a PR with your changes and a clear description of the changes.
