#!/bin/bash

TARGET=$1

run_uvicorn () {
    cd $TARGET
    poetry run gunicorn main:app -k uvicorn.workers.UvicornWorker -c gunicorn.py
}

execute_autocannon () {
    [ ! -d "./results" ]  && mkdir -p results
    for i in {1..10}; do
        for ENDPOINT in square-sync square-async json plaintext; do
            npx autocannon -j "http://0.0.0.0:8001/$ENDPOINT" >> "./results/${TARGET}-${ENDPOINT}-${i}.json"
        done
    done
}

run_uvicorn &
printf "waiting for 5 seconds before executing tests\n\n"
sleep 5
execute_autocannon
kill $!
printf "\n\ntest sequence finished"
