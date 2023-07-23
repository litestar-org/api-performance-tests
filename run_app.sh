#!/bin/bash

uvicorn --no-access-log --loop uvloop app:app --host 0.0.0.0 --port 8081 --timeout-keep-alive 15
