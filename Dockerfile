FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

ENV LANG en_US.utf8

EXPOSE 8000
ADD . /code/