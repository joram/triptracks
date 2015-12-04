FROM ubuntu:15.04
MAINTAINER John Oram <john@oram.ca>

RUN locale-gen --no-purge en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python python-pip
RUN apt-get -y install build-essential autoconf libtool pkg-config python-dev
RUN apt-get -y install binutils libproj-dev gdal-bin
RUN apt-get -y install postgresql-9.4 postgresql-9.4-postgis postgresql-server-dev-9.4


RUN pip install Django==1.8
RUN pip install jsonfield
RUN pip install django_admin_bootstrapped
RUN pip install django-geoip
RUN pip install django-tastypie
RUN pip install psycopg2==2.6.1

#########
# create user/password/db:
#  - tp_user
#  - tp_password
#  - tp_database
#########
USER postgres
RUN service postgresql start && psql --command "CREATE USER tp_user WITH SUPERUSER PASSWORD 'tp_password';" && createdb -O tp_user tp_database

USER root
RUN mkdir /srv/www/
RUN mkdir -p /srv/www/trip-planner
ENV PYTHONPATH /srv/www/trip-planner/trip_planner_www
ENV DJANGO_SETTINGS_MODULE trip_planner_www.settings

ADD . /srv/www/trip-planner

RUN service postgresql start && django-admin.py syncdb --noinput && django-admin.py makemigrations && django-admin.py migrate && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | django-admin.py shell

EXPOSE 8000
VOLUME /srv/www/trip-planner
WORKDIR /srv/www/trip-planner
CMD service postgresql start && django-admin.py runserver 0.0.0.0:8000
