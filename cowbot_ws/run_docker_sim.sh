#!/bin/bash

# Setup X11 authentication for Docker
XAUTH=/tmp/.docker.xauth
if [ ! -f $XAUTH ]; then
    touch $XAUTH
    xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
    chmod 644 $XAUTH
fi

# Allow Docker to connect to X server
xhost +local:docker

# Build and run the Docker container
sudo docker-compose up --build

# Cleanup
xhost -local:docker
