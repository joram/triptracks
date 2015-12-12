FROM ubuntu:15.10
MAINTAINER John Oram <john@oram.ca>

#########
# install all aptitude packages
#########
RUN apt-get -y update
RUN apt-get -y upgrade
ADD requirements_apt.txt /requirements_apt.txt
RUN cat /requirements_apt.txt | xargs apt-get install -y

#########
# install all pip packages
#########
ADD requirements_pip.txt /requirements_pip.txt
RUN pip install -r /requirements_pip.txt


USER root
RUN mkdir /srv/www/
RUN mkdir -p /srv/www/trip-planner
ENV PYTHONPATH /srv/www/trip-planner/trip_planner_www
ENV DJANGO_SETTINGS_MODULE trip_planner_www.settings

EXPOSE 8000
VOLUME /srv/www/trip-planner
WORKDIR /srv/www/trip-planner

#COPY ./entrypoint.sh /entrypoint.sh
#CMD ["/entrypoint.sh"]

CMD ["cat", "/etc/hosts", "&&", "django-admin.py", "runserver", "0.0.0.0:8000"]