FROM python:3.9.0-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app
  
RUN python -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
