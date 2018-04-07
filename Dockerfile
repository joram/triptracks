FROM ecarrara/python-gdal

RUN rm -rf /var/lib/apt/lists/*

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


CMD python /code/manage.py runserver 0.0.0.0:$PORT
#CMD gunicorn wsgi:application --bind=0:$PORT --access-logfile=- --error-logfile=-
