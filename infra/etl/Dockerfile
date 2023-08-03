FROM python:3.11-slim

ENV SRC_DIR=/opt
ENV ETL_DIR=$SRC_DIR/etl

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
RUN poetry install --no-root

WORKDIR $ETL_DIR

COPY ./src/etl $ETL_DIR

CMD poetry run python3 main.py
