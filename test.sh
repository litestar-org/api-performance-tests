#!/bin/bash

set -e

for TARGET in v1.20.0 main performance_updates; do
    rm -f results.bin
    pip install git+https://github.com/starlite-api/starlite.git@$TARGET
    (gunicorn main:app -k uvicorn.workers.UvicornWorker -c gunicorn.config.py) &
    printf "\n\nwaiting for service to become available\n\n"
    sleep 5
    printf "\n\ninitializing test sequence for $TARGET\n\n"
    endpoints=(
        "async-plaintext-mixed-params/256?first=128"
        "async-plaintext-no-params"
        "async-plaintext-query-param?first=128"
        "async-plaintext/128"
    )
    for ENDPOINT in "${endpoints[@]}"; do
        name=$(echo "${TARGET}-${ENDPOINT}.json" | sed 's/^\///;s/\//-/g')
        printf "\n\nrunning test $name\n\n"
        ./bombardier "http://0.0.0.0:8001/$ENDPOINT" --duration=10s --format=json --print=result >> "./results/$name"
    done
    printf "\n\ntest sequence finished\n\nterminating all running gunicorn instances\n\n"
    pkill gunicorn
done

python ./analysis/analyzer.py
printf "\n\nTests Finished Successfully!"
