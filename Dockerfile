FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY ./repositorium /repositorium/repositorium
COPY ./manage.py /repositorium/
COPY ./requirements.txt /repositorium/
COPY ./repositorium.sh /repositorium/

RUN chmod -R 755 /repositorium/
WORKDIR /repositorium/

RUN apt-get update
RUN pip install -r requirements.txt
RUN adduser repositorium
USER repositorium
RUN echo "source /repositorium/repositorium.sh" >> ~/.bashrc

CMD gunicorn Repositorium.wsgi:application --bind 0.0.0.0:$PORT
