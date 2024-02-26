FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install gcc libpq-dev python3-dev -y && apt-get autoclean

COPY ./requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY src /app
