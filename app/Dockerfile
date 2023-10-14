FROM ubuntu:20.04

RUN mkdir /code
RUN mkdir /code/data
WORKDIR /code

COPY . . 

RUN chmod 0644 /code
RUN apt update
RUN apt install -y cron
RUN apt install -y python3-pip
RUN pip install requests

RUN python3 create_tables.py

RUN crontab /code/crontab.txt

CMD cron

