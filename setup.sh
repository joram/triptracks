#!/bin/bash

export CODE_DIR=~/code
if [ ! -d $CODE_DIR ]; then
  mkdir $CODE_DIR
fi;
export POSTGIS_DIR=$CODE_DIR/postgis
export ELASTIC_DIR=$CODE_DIR/elasticsearch
export PROJECT_DIR=$CODE_DIR/trip-planner

if [ ! -d $POSTGIS_DIR ]; then
    cd $CODE_DIR
    git clone https://github.com/joram/postgis.git
fi;
cd $POSTGIS_DIR
git pull --rebase

if [ ! -d $ELASTIC_DIR ]; then
    cd $CODE_DIR
    git clone https://github.com/joram/elasticsearch.git
fi;
cd $ELASTIC_DIR
git pull --rebase

echo making: $POSTGIS_DIR
sudo docker build -t tp/postgis $POSTGIS_DIR
echo making: $ELASTIC_DIR
sudo docker build -t tp/elastic $ELASTIC_DIR
echo making: $PROJECT_DIR
sudo docker build -t tp/tripplanner $PROJECT_DIR
