#!/bin/bash

set -e

for TARGET in v1.20.0 v1.39.0; do
    pip install git+https://github.com/starlite-api/starlite.git@$TARGET
    (uvicorn --no-access-log --loop uvloop main:app) &
    printf "\n\nwaiting for service to become available\n\n"
    sleep 2
    printf "\n\ninitializing test sequence for $TARGET\n\n"
    endpoints=(
        "async-plaintext-mixed-params/256?first=128"
        "async-plaintext-no-params"
        "async-plaintext-query-param?first=128"
        "async-plaintext/128"
    )
    for ENDPOINT in "${endpoints[@]}"; do
        name=$(echo "${TARGET}-${ENDPOINT}.json" | sed 's/^\///;s/\//-/g')
        printf "warming up endpoints\n"
        ./bombardier "http://0.0.0.0:8000/$ENDPOINT" --duration=5s --no-print
        printf "\n\nrunning test $name\n\n"
        ./bombardier "http://0.0.0.0:8000/$ENDPOINT" --duration=30s --format=json --print=result >> "./results/$name"
    done
    printf "\n\ntest sequence finished\n\nterminating all running uvicorn instances\n\n"
    pkill uvicorn
done

python ./analyze.py
printf "\n\nTests Finished Successfully!"