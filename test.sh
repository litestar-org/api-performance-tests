#!/bin/bash

set -e
[ -d "./results" ] && rm -rf results
mkdir -p results

[ ! -d "./.vent" ] && python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt

for TARGET in starlette starlite fastapi; do
  (cd $TARGET && gunicorn main:app -k uvicorn.workers.UvicornWorker -c gunicorn.py) &
  printf "waiting for 10 seconds before initiating test sequence\n\n"
  sleep 5
  for i in {1..4}; do
    for ENDPOINT in json-async json-sync 1 query-param?value=2; do
      npx autocannon -c 30 -w 4 -j "http://0.0.0.0:8001/$ENDPOINT" >>"./results/${TARGET}-${ENDPOINT}-${i}.json"
    done
  done
  printf "\n\ntest sequence finished\nterminating all running python instances"
  killall python
done

[ -f ./result.png ] && rm ./result.png
python analysis/analyzer.py
printf "\n\ngenerated 'result.png'\n\nTests Finished Successfully!"
