FROM python:3.10.8-alpine3.15

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache mariadb-connector-c-dev && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base mariadb-dev musl-dev busybox-suid && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home django

ENV PATH="/py/bin:$PATH"

USER django

