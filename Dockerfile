FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN apk update && apk -y add \
	python3-devel postgresql-devel

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
