#!/bin/bash

./build.sh
./run.sh bench-frameworks --frameworks all
./run.sh analyze
