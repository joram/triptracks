#!/bin/bash

# TODO: move to code dir
mkdir ~/code
export CODE_DIR=~/code
export POSTGIS_DIR=~/code/postgis
export ELASTICSEARCH_DIR=~/code/elasticsearch

# create postgis docker image
cd $CODE_DIR
if [ ! -d $POSTGIS_DIR ]; then
    git clone https://github.com/joram/postgis.git
fi;
cd $POSTGIS_DIR
git pull --rebase
sudo docker build -t postgis .

# create elastic docker image
cd $CODE_DIR
if [ ! -d $ELASTICSEARCH_DIR ]; then
    git clone https://github.com/joram/elasticsearch.git
fi;
cd $ELASTICSEARCH_DIR
git pull --rebase
sudo docker build -t elasticsearch .
