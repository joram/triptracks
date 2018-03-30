# TripTracks
This project is under development. The goal is to have a unified site to manage trip plans and reports for outdoor trips.

## Setup
- pull the project: `git clone https://github.com/joram/trip-planner.git`
- install the project dependencies
```bash
sudo apt-get install libgdal-dev
pip install -r requirements.txt
```
- build the docker container `bash ./scripts/services/start`
- migrate your database `python ./scripts/manage migrate`
- run the server `bash ./scripts/run`
- (optional) load in some gpx files with `python ./scripts/load/trailpeak`
- visit in the browser <a href="http://localhost:8000">localhost:8000</a>

### pyenv
- install pyenv `curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`
- install python `pyenv install 2.7.14`
- 


#### notes:
- if you need to clean up space:
  - Delete all containers `sudo docker rm $(sudo docker ps -a -q)`
  - Delete all images `sudo docker rmi $(sudo docker images -q)`
  - if you really need to scrub, docker's temp folder is at `/var/lib/docker/tmp`
