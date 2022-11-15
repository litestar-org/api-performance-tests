FROM python:3.11-slim-bullseye as build

COPY pyproject.toml poetry.lock /

RUN apt-get update && apt-get install -y curl git gcc procps && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
    curl -sSL https://github.com/codesenberg/bombardier/releases/download/v1.2.5/bombardier-linux-amd64 -o bombardier && \
    chmod +x bombardier && \
    pip install --upgrade pip && \
    pip install cython && \
    pip install wheel && \
    /opt/poetry/bin/poetry config virtualenvs.create false && \
    /opt/poetry/bin/poetry update && \
    /opt/poetry/bin/poetry export --without-hashes --format requirements.txt --output requirements.txt && \
    pip install -r requirements.txt

FROM build

COPY frameworks/ /frameworks/
COPY analyze.py cli.py /

ENTRYPOINT ["python", "./cli.py"]