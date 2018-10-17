FROM alpine:3.4

RUN apk add --no-cache --virtual .crypto-rundeps --repository http://dl-cdn.alpinelinux.org/alpine/edge/main libressl2.7-libcrypto
RUN apk add --no-cache gdal geos --repository http://nl.alpinelinux.org/alpine/edge/testing
RUN apk add --update python python-dev linux-headers py-pip postgresql-dev gcc make musl-dev build-base libxml2-dev libxslt-dev git
RUN rm -rf /var/lib/apt/lists/*
RUN pip install pip --upgrade

RUN mkdir /code
RUN mkdir /code/apps
RUN mkdir /code/scrapers
RUN mkdir /code/settings
RUN mkdir /code/utils

ADD requirements.txt /code
ADD manage.py /code
ADD urls.py /code
ADD wsgi.py /code

WORKDIR /code
RUN pip install -r requirements.txt
RUN rm -rf /root/.cache/pip/wheels/*

ADD ./apps/. /code/apps
ADD ./scrapers/. /code/scrapers
ADD ./settings/. /code/settings
ADD ./utils/. /code/utils

RUN export GEOS_LIBRARY_PATH=/usr/lib/libgeos-3.6.2.so
RUN export GDAL_LIBRARY_PATH=/usr/lib/libgdal.so.20

RUN mkdir settings/static
RUN export DJANGO_SETTINGS_MODULE=settings.prod; python /code/manage.py collectstatic

CMD gunicorn wsgi:application --bind=0:$PORT --access-logfile=- --error-logfile=-
