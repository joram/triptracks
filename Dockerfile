FROM ecarrara/python-gdal

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code/

CMD ./manage.py runserver 0.0.0.0:8000
#CMD gunicorn wsgi:application --bind=0:$PORT --access-logfile=- --error-logfile=-
