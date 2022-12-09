FROM python:3.9.0-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN sudo yum install python3-devel postgresql-devel

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
