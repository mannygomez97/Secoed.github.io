FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt
ADD . /code/