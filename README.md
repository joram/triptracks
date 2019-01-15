# Triptracks
This project is under development. The goal is to have a unified site to manage trip plans and reports for outdoor trips.

## Setup
- pull the project: `git clone https://github.com/joram/triptracks.git`

![Alt text](https://g.gravizo.com/source/triptracks_tldr?https%3A%2F%2Fraw.githubusercontent.com%2Fjoram%2Ftriptracks%2Fmaster%2FREADME.md)
<details> 
<summary></summary>
triptracks_tldr
  digraph G {
    React Client [shape=box];
    React Client -> GraphQL Lambda;
    GraphQL Lambda -> Django Models;
    GraphQL Lambda -> Geohash S3 Routes Store;
  }
triptracks_tldr
</details>

### pyenv
- install pyenv `curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash`
- install python
    ```
    pyenv install 3.6.6
    pyenv virtualenv 3.6.6 tt
    pyenv activate tt
    pip install -r requirements.txt
    ```

### secrets
create the file `scripts/.env`
inside it add:
```
TT_GOOGLE_MAPS_API_KEY=...
TT_GOOGLE_CLIENT_ID=...
TT_DATABASE_URL=postgresql://docker:docker@localhost:25432/tripplanner
TT_STRAVA_CLIENT_SECRET=...
TT_STRAVA_ACCESS_TOKEN=...
TT_STRAVA_REFRESH_TOKEN=...
PORT=8000
```

#### notes:
- if you need to clean up space:
  - Delete all containers `sudo docker rm $(sudo docker ps -a -q)`
  - Delete all images `sudo docker rmi $(sudo docker images -q)`
  - if you really need to scrub, docker's temp folder is at `/var/lib/docker/tmp`
