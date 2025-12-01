#!/bin/bash

# Setup X11 authentication for Docker
XAUTH=/tmp/.docker.xauth
if [ -f $XAUTH ]; then
    sudo rm -f $XAUTH
fi
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
chmod 644 $XAUTH

# Allow Docker to connect to X server
xhost +local:docker

# Run interactive shell in Docker container
sudo docker run -it --rm \
    --name cowbot_dev \
    --network host \
    --privileged \
    -e DISPLAY=$DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -e XAUTHORITY=/tmp/.docker.xauth \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v /tmp/.docker.xauth:/tmp/.docker.xauth:rw \
    -v $(pwd):/workspace:rw \
    -v /dev/dri:/dev/dri \
    cowbot_gazebo:latest \
    /bin/bash

# Cleanup
xhost -local:docker
