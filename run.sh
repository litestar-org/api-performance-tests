#!/bin/bash

docker run -it -v "$PWD/results:/results" starlite-api-benchmarks "$@"
