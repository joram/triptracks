FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update ; apt-get --assume-yes install binutils libproj-dev gdal-bin

RUN wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
RUN tar -xjf geos-3.4.2.tar.bz2
RUN cd geos-3.4.2; ./configure; make; make install

RUN wget http://download.osgeo.org/gdal/1.11.0/gdal-1.11.0.tar.gz
RUN tar -xzf gdal-1.11.0.tar.gz
RUN cd gdal-1.11.0; ./configure; make; make install

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code/

CMD ./manage.py runserver 0.0.0.0:8000
#CMD gunicorn wsgi:application --bind=0:$PORT --access-logfile=- --error-logfile=-
EOF
