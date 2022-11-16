#!/bin/bash

./build.sh
./run.sh bench -e async -t plaintext rps --frameworks all
./run.sh analyze
