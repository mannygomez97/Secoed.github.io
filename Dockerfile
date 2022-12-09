FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r requirements.txt
