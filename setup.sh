#!/bin/bash

#sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
#sudo rm /etc/apt/sources.list.d/docker.list
#sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list
#sudo apt-get update
#sudo apt-get install docker-engine


export CODE_DIR=~/code
export PROJECT_DIR=$CODE_DIR/trip-planner

if [ ! -d $CODE_DIR ]; then
  mkdir $CODE_DIR
fi;

if [ ! -d $PROJECT_DIR/data ]; then
  mkdir $PROJECT_DIR/data
fi;

if [ ! -d $PROJECT_DIR/data/postgresql ]; then
  mkdir $PROJECT_DIR/data/postgresql
  chmod 777 -R $PROJECT_DIR/data/postgresql
fi;

if [ ! -d $PROJECT_DIR/data/elasticsearch ]; then
  mkdir $PROJECT_DIR/data/elasticsearch
fi;

sudo docker stop db
sudo docker rm db
sudo docker pull kartoza/postgis
#TODO: figure out permissions for data/postgresql before mounting it as a vol
sudo docker run -d --name=db -p 5432 -e POSTGRES_USER=tp_user -e POSTGRES_PASS=tp_password -t kartoza/postgis

sudo docker stop search
sudo docker rm search
sudo docker pull elasticsearch
sudo docker run -d --name=search -v $PROJECT_DIR/data/elasticsearch:/usr/share/elasticsearch/data -p 9200:9200 -p 9300:9300 elasticsearch

sudo service nginx stop
sudo docker stop web
sudo docker wait web
sudo docker rm web
sudo docker build -t joram/tripplanner $PROJECT_DIR
sudo docker run -ti --name=web -p 80:80 -p 8000:8000 --link db:db --link search:search -v $PROJECT_DIR:/srv/www joram/tripplanner

