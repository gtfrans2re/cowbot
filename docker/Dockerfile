FROM osrf/ros:jazzy-desktop-full

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DOMAIN_ID=0
ENV ROS_LOCALHOST_ONLY=0

# Install simulation dependencies
# Note: ros-jazzy-desktop-full already includes most ROS 2 packages
# For ROS 2 Jazzy, we use Ignition Gazebo (gz-jazzy) instead of ros-gazebo packages
RUN apt-get update && apt-get install -y \
    gz-jazzy \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport \
    ros-jazzy-image-transport-plugins \
    ros-jazzy-tf2-tools \
    ros-jazzy-rqt \
    ros-jazzy-rqt-common-plugins \
    ros-jazzy-rqt-tf-tree \
    ros-jazzy-tf2-ros \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-xacro \
    python3-pip \
    python3-colcon-common-extensions \
    wget \
    curl \
    git \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    opencv-python-headless \
    numpy || true

# Set up workspace directory
WORKDIR /ros2_ws

# Note: Workspace will be mounted as volume from docker-compose.yml at runtime
# No need to copy or build here - it's mounted live for development

# Set up entrypoint script
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'source /opt/ros/jazzy/setup.bash' >> /entrypoint.sh && \
    echo 'if [ -f /ros2_ws/install/setup.bash ]; then' >> /entrypoint.sh && \
    echo '    source /ros2_ws/install/setup.bash' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo 'exec "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Default command
CMD ["/entrypoint.sh"]
