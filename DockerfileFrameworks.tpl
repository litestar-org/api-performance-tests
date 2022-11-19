FROM python:3.11-slim-bullseye as build


RUN apt-get update && apt-get upgrade -y && apt-get install gcc git -y && \
    pip install --upgrade pip && \
    pip install uvicorn uvloop


FROM build
ARG RANDOM_STRING=1

COPY frameworks/{framework}_app.py /app.py
COPY test_data/ /test_data/

RUN pip install {pip_package}

CMD ["uvicorn", "--no-access-log", "--loop", "uvloop", "app:app", "--host", "0.0.0.0", "--port", "8081"]
