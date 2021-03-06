FROM python:3.8-slim

LABEL maintainer="Johannes Krumm <jkrumm@algorithmiccrypto.com>"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt --no-cache-dir

COPY . /code
WORKDIR /code

EXPOSE 5000
