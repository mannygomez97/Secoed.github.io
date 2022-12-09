FROM python:3.9.0-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN yum update -y

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
