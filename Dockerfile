FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

RUN python3 -m ensurepip

RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
