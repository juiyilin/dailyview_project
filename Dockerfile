# syntax=docker/dockerfile:1
FROM python:3.7

WORKDIR /home/dailyview

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y libgl1 && apt-get -y install cron && apt-get -y install nano
RUN pip install -r requirements.txt

COPY . /home/dailyview
