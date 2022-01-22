#!/bin/bash

[ -d "./results" ] && rm -rf results
mkdir -p results

[ ! -d "./.vent" ] && python -m venv .venv
pip3 install -r requirements.txt

for TARGET in starlite fastapi; do
    (cd $TARGET && gunicorn main:app -k uvicorn.workers.UvicornWorker -c gunicorn.py) &
    SUBSHELL_PID=$!
    printf "waiting for 5 seconds before executing tests\n\n"
    sleep 5
    for i in {1..4}; do
        for ENDPOINT in square-sync square-async json plaintext; do
            npx autocannon -c 25 -w 4 -j "http://0.0.0.0:8001/$ENDPOINT" >> "./results/${TARGET}-${ENDPOINT}-${i}.json"
        done
    done
    kill $SUBSHELL_PID
    printf "\n\ntest sequence finished"
done

[ -f "./result.png" ] && rm ./result.png
python analysis/analyzer.py
printf "\n\ngenerated ./result.png\nTests Finished"
