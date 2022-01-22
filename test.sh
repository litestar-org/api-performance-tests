#!/bin/bash

TARGET=$1

run_uvicorn () {
    cd $TARGET
    poetry run gunicorn main:app -k uvicorn.workers.UvicornWorker -c gunicorn.py
}

execute_autocannon () {
    [ ! -d "./results" ]  && mkdir -p results
    for ENDPOINT in square-sync square-async json plaintext; do
        npx autocannon -d 10 -c 60 -w 4 -j "http://0.0.0.0:8001/$ENDPOINT" >> "./results/${TARGET}-${ENDPOINT}.json"
    done
}

run_uvicorn &
printf "waiting for 5 seconds before executing tests\n\n"
sleep 5
execute_autocannon
kill $!
printf "\n\ntest sequence finished"
