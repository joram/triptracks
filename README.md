# trip-planner
This project is under development. The goal is to have a unified site to manage trip plans and reports for outdoor trips.

## Setup

### Git
pull the project: `git clone https://github.com/joram/trip-planner.git`

### Docker
- to build your local docker image run: `sudo docker build -t tripplanner .`
- run the container (in the foreground): `sudo docker run --rm -p 8000:8000 -v <absolute_path_to_code_base>:/srv/www/trip-planner -t tripplanner`
  - Note: The --rm removes the container and its image when the container exits successfully.
- visit in the browser <a href="http://localhost:8000">localhost:8000</a>
- if you need to restart the docker instance: `sudo service docker restart`
- if you need to clean up space:
  - Delete all containers `sudo docker rm $(sudo docker ps -a -q)`
  - Delete all images `sudo docker rmi $(sudo docker images -q)`