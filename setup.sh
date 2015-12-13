#!/bin/bash

#sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
#sudo rm /etc/apt/sources.list.d/docker.list
#sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list
#sudo apt-get update
#sudo apt-get install docker-engine


export CODE_DIR=~/code
if [ ! -d $CODE_DIR ]; then
  mkdir $CODE_DIR
fi;
export POSTGIS_DIR=$CODE_DIR/postgis
export ELASTIC_DIR=$CODE_DIR/elasticsearch
export PROJECT_DIR=$CODE_DIR/trip-planner

if [ ! -d $POSTGIS_DIR ]; then
    cd $CODE_DIR
    git clone git://github.com/joram/postgis
fi;
cd $POSTGIS_DIR
git pull --rebase

if [ ! -d $ELASTIC_DIR ]; then
    cd $CODE_DIR
    git clone https://github.com/joram/elasticsearch.git
fi;
cd $ELASTIC_DIR
git pull --rebase

sudo docker build -t tp/postgis $POSTGIS_DIR
sudo docker build -t tp/tripplanner $PROJECT_DIR

sudo docker stop db
sudo docker rm db
sudo docker run -d --name=db -p 5432:5432 tp/postgis

sudo docker stop web
sudo docker rm web
sudo docker run -d --name=web -p 8000:8000 --link db:db -v /home/joram/code/trip-planner:/srv/www tp/tripplanner
