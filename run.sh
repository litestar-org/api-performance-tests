#!/bin/bash

rm -rf results
mkdir results
docker build . -t starlite-api-benchmarks
#docker run -it -v "$PWD/results:/results" starlite-api-benchmarks bench starlite
docker run -it -v "$PWD/results:/results" starlite-api-benchmarks "$@"