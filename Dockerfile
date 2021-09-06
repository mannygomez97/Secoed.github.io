FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python3 -m venv /opt/venv
RUN . /opt/venv/bin/activate
RUN pip install -r requirements.txt
ADD . /code/
RUN python manage.py makemigrations
RUN python mange.py migrate