#!/bin/bash
set -e

# Source ROS 2 setup
source /opt/ros/jazzy/setup.bash

# Source workspace if it exists
if [ -f /ros2_ws/install/setup.bash ]; then
    source /ros2_ws/install/setup.bash
fi

# Execute command passed to container
exec "$@"

