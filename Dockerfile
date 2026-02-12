FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN python -m pip install -U pip \
    && pip install -e ".[dev]"

CMD ["echonull-orchestrator", "--runs", "5", "--thresholds", "0.25,0.5", "--out", "/out", "--workers", "1", "--zip"]
