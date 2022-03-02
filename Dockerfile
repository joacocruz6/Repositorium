FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY ./Repositorium /repositorium/Repositorium
COPY ./manage.py /repositorium/
COPY ./requirements.txt /repositorium/


RUN chmod -R 755 /repositorium/
WORKDIR /repositorium/

RUN apt-get update
RUN pip install -r requirements.txt
RUN adduser repositorium
USER repositorium

CMD gunicorn Repositorium.wsgi:application --bind 0.0.0.0:$PORT
