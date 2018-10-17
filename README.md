# TripTracks
This project is under development. The goal is to have a unified site to manage trip plans and reports for outdoor trips.

## Associated Resources:
[dockerhub image](https://hub.docker.com/r/joram87/triptracks/)

## Setup
- pull the project: `git clone https://github.com/joram/trip-planner.git`
- install the project dependencies
```bash
sudo apt-get install libgdal-dev
```

### pyenv
- install pyenv `curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`
- install python
    ```
    pyenv install 2.7.14
    pyenv virtualenv 2.7.14 tt
    pyenv activate tt
    pip install -r requirements.txt
    ```

### More Setup
- build the docker container `bash ./scripts/services/start`
- migrate your database `./scripts/manage migrate`
- run the server `./scripts/run`
- (optional) load in some gpx files with `./scripts/load/routes` and `./scripts/load/items`
- visit in the browser <a href="http://localhost:8000">localhost:8000</a>

### secrets
create the file `scripts/.env`
inside it add:
```
TP_GOOGLE_MAPS_API_KEY=...
TP_GOOGLE_CLIENT_ID=...
TP_DATABASE_URL=postgresql://docker:docker@localhost:25432/tripplanner
```

#### notes:
- if you need to clean up space:
  - Delete all containers `sudo docker rm $(sudo docker ps -a -q)`
  - Delete all images `sudo docker rmi $(sudo docker images -q)`
  - if you really need to scrub, docker's temp folder is at `/var/lib/docker/tmp`
