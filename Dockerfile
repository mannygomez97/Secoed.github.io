# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
