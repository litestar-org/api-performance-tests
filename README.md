# api-performance-tests

To execute the tests:

1. make sure you have python 3.10+ installed and [poetry](https://python-poetry.org/).
2. you must first install the dependencies for both `starlite` and `fastAPI` by going into their respective directories and executing `poetry install`.
3. install autocannon by executing `npm install` in the root folder.

Once these are all done, you can execute the tests by running `./test.sh starlite` and `./test.sh fastapi` respectively. The tests are setup to output the data as json files saved under the `results folder`.

## Updating dependencies

To update dependencies simply run `poetry update` in both the `starlite` and `fastapi folders`

## Contributing

Please make sure to install [pre-commit](https://pre-commit.com/) on your system, and then execute `pre-commit install` in the repository root - this will ensure the pre-commit hooks are in place.

After doing this, add a PR with your changes and a clear description of the change.
