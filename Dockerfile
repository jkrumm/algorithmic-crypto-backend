FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
STOPSIGNAL SIGTERM

RUN apk update && apk upgrade

RUN apk add gcc --no-cache

RUN apk add --virtual build-deps postgresql-dev gcc musl-dev --update-cache --no-cache

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install pip --upgrade && pip install -r requirements.txt --no-cache-dir
