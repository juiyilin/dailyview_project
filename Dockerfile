# syntax=docker/dockerfile:1
FROM python:3.7

WORKDIR /home/dailyview
COPY wait-for-it.sh wait-for-it.sh
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y libgl1 && apt-get -y install cron && apt-get -y install nano
RUN pip install -r requirements.txt

COPY ./app /home/dailyview
COPY .env /home/dailyview/
