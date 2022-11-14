#!/bin/bash

rm -rf results
mkdir results
docker build . -t starlite-api-benchmarks
docker run -v "$PWD/results:/results" starlite-api-benchmarks