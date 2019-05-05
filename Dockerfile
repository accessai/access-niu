FROM python:3.6-slim

ADD . /access-niu
WORKDIR /access-niu
RUN pip install /access-niu

EXPOSE 8000

