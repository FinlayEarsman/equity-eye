FROM python:3.10.9-slim-buster

COPY src .
COPY requirements.txt .

RUN python -m venv /py && \
    apt-get update && \
    apt-get install vim -y && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"

RUN chmod +x create_assets.py && \
    chmod +x fetch_new_aggregates.py

CMD sleep 1d
