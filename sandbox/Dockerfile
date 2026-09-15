FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd \
    --create-home \
    --uid 1000 \
    --shell /usr/sbin/nologin \
    sandbox

WORKDIR /workspace

USER sandbox