FROM python:3.9-slim

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

COPY ./requirements.txt ./MANIFEST.in ./VERSION ./project.py ./setup.py ./
COPY mammon_api/ ./mammon_api

RUN python -m venv /venv

RUN /venv/bin/python setup.py install

EXPOSE 7000

ENTRYPOINT ["venv/bin/uvicorn", "mammon_api.api:app", "--host", "0.0.0.0", "--port", "7000"]
