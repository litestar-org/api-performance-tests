#!/bin/bash

TARGET=$1

run_uvicorn () {
    cd $TARGET
    poetry run gunicorn main:app -k uvicorn.workers.UvicornWorker -c gunicorn.py
}

execute_autocannon () {
    npx autocannon http://0.0.0.0:8001/square-sync
    npx autocannon http://0.0.0.0:8001/square-async
    npx autocannon http://0.0.0.0:8001/json
    npx autocannon http://0.0.0.0:8001/plaintext
}

run_uvicorn &
echo "waiting for 5 seconds before executing tests"
sleep 5
execute_autocannon
kill $!
echo "finished"
