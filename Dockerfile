FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN adduser repositorium
USER repositorium