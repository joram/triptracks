# trip-planner
## Description
This project is under development. The goal is to have a unified site to manage trip plans and reports for outdoor trips.

## Setup
### Docker
#### to build your local docker image run:
`sudo docker build -t tripplanner .`
#### And run the container (in the foreground):
`sudo docker run --rm -p 8000:8000 -t tripplanner`
Note: The --rm removes the container and its image when the container exits successfully.
