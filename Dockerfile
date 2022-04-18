FROM python:3.9-slim as build-stage

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

COPY ./requirements.txt ./MANIFEST.in ./VERSION ./setup.py ./
COPY mammon_api/ ./mammon_api

RUN python -m venv /venv

RUN /venv/bin/python setup.py install

FROM python:3.9-slim

COPY --from=build-stage /venv /venv

ENTRYPOINT ["/venv/bin/python3", "-m", "mammon_api"]