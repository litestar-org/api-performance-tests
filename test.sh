#!/bin/bash

set -e

[ -d "./results" ] && rm -rf results
mkdir -p results

pnpm --version || npm i -g pnpm
pnpm up

poetry --version || (curl -sSL https://install.python-poetry.org | python3 -)
poetry update

[ ! -d "./venv" ] &&
python -m venv .venv &&
source .venv/bin/activate &&
pip install --upgrade pip &&
pip install cython &&
pip install wheel &&
poetry export --without-hashes --format requirements.txt --output requirements.txt &&
pip install -r requirements.txt && rm requirements.txt;

for TARGET in starlite starlette fastapi sanic blacksheep; do
    (cd "$TARGET" && gunicorn main:app -k uvicorn.workers.UvicornWorker -c gunicorn.config.py) &
    printf "\n\nwaiting for service to become available\n\n"
    sleep 5
    printf "\n\ninitializing test sequence for $TARGET\n\n"
    endpoints=(
        "async-plaintext-no-params"
        "sync-plaintext-no-params"
        "async-plaintext/128"
        "sync-plaintext/128"
        "async-plaintext-query-param?first=128"
        "sync-plaintext-query-param?first=128"
        "async-plaintext-mixed-params/256?first=128"
        "sync-plaintext-mixed-params/256?first=128"
    )
    for i in {1..2}; do
        for ENDPOINT in "${endpoints[@]}"; do
            name=$(echo "${TARGET}-${ENDPOINT}-${i}.json" | sed 's/^\///;s/\//-/g')
            printf "\n\nrunning test $name\n\n"
            pnpm autocannon -j "http://0.0.0.0:8001/$ENDPOINT" >>"./results/$name"
        done
    done
    printf "\n\ntest sequence finished\n\nterminating all running python instances\n\n"
    pkill python
done

[ -f "./result.png" ] && rm "./result.png"
python analysis/analyzer.py
printf "\n\nTests Finished Successfully!"
deactivate
