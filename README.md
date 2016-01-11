# trip-planner
This project is under development. The goal is to have a unified site to manage trip plans and reports for outdoor trips.

## Setup

### Git
pull the project: `git clone https://github.com/joram/trip-planner.git`

### Gulp coffee
- install gulp `sudo npm install gulp gulp-coffee`
- from the base code dir, run `gulp coffee`

### Docker
- to build docker images and run django container in foreground: `./setup.sh`
:/srv/www/trip-planner -t tripplanner`
- visit in the browser <a href="http://localhost:8000">localhost:8000</a>

#### notes:
- if you need to restart the docker instance: `sudo service docker restart`
- if you need to clean up space:
  - Delete all containers `sudo docker rm $(sudo docker ps -a -q)`
  - Delete all images `sudo docker rmi $(sudo docker images -q)`
  - if you really need to scrub, docker's temp folder is at `/var/lib/docker/tmp`
