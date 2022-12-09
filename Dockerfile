# base image
FROM python:3.9.7-buster
 
# options
ENV PYTHONUNBUFFERED 1
 
# coppy commands 
WORKDIR /usr/src/app
 
# update docker-iamage packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean
 
# update pip 
RUN pip install --upgrade pip
# install psycopg for connect to pgsql
RUN pip install psycopg2-binary
# install python packages
COPY requirements.txt ./
RUN pip install -r requirements.txt
