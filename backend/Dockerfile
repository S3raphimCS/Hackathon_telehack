# syntax=docker/dockerfile:1.4

FROM python:3.10-alpine3.16

ENV PYTHONUNBUFFERED=1
COPY /requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

COPY SPO_KROT/ /api
WORKDIR /api

RUN adduser --disabled-password --no-create-home django
USER django


COPY ./entrypoint.sh / 
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
