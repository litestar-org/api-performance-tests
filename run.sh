#!/bin/bash

rm -rf results
mkdir results
docker run -it -v "$PWD/results:/results" starlite-api-benchmarks "$@"