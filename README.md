# Triptracks
This project is under development. The goal is to have a unified site to manage trip plans and reports for outdoor trips.

The high level architecture is:
- A react client, that makes graphql calls to get its data from the server
- A graphql server, running in lambda, backed by a postgres DB and a geohash S3 storage mechanism.

![Alt text](https://g.gravizo.com/source/triptracks_tldr?https%3A%2F%2Fraw.githubusercontent.com%2Fjoram%2Ftriptracks%2Fmaster%2FREADME.md)
<details> 
<summary></summary>
triptracks_tldr
  digraph G {
    "React Client";
    "React Client" -> "GraphQL Lambda";
    "GraphQL Lambda" -> "Django Models" [shape=cylinder];
    "GraphQL Lambda" -> "Geohash S3 Routes Store"  [shape=cylinder];
  }
triptracks_tldr
</details>

## Client
### environment setup
```
cd ./client
npm install -g
```
### running
```
cd ./client
npm run start
```

## Server
### environment setup
- install pyenv `curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`
- install python
    ```
    pyenv install 3.6.6
    pyenv virtualenv 3.6.6 tt
    pyenv activate tt
    pip install -r requirements.txt
    ```
- create the file `scripts/.env` and inside it add:
    ```
    TT_GOOGLE_MAPS_API_KEY=...
    TT_GOOGLE_CLIENT_ID=...
    TT_DATABASE_URL=postgresql://docker:docker@localhost:25432/tripplanner
    TT_STRAVA_CLIENT_SECRET=...
    TT_STRAVA_ACCESS_TOKEN=...
    TT_STRAVA_REFRESH_TOKEN=...
    PORT=8000
    ```
### running
```
source ./scripts/.env
cd ./server
./manage.py runserver
```

#### notes:
- if you need to clean up space:
  - Delete all containers `sudo docker rm $(sudo docker ps -a -q)`
  - Delete all images `sudo docker rmi $(sudo docker images -q)`
  - if you really need to scrub, docker's temp folder is at `/var/lib/docker/tmp`
