FROM python:3.9-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get -y install \
	python-pip python-dev

COPY requirements.txt ./

RUN pip install -r requirements.txt
