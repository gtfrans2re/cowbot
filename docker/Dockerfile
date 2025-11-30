FROM osrf/ros:jazzy-desktop-full

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DOMAIN_ID=0
ENV ROS_LOCALHOST_ONLY=0

# Install Gazebo and simulation dependencies
RUN apt-get update && apt-get install -y \
    ros-jazzy-gazebo-ros-pkgs \
    ros-jazzy-gazebo-ros2-control \
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
    numpy

# Set up workspace directory
WORKDIR /ros2_ws

# Copy workspace source (will be mounted as volume, but copy for initial build)
# This allows the Dockerfile to be built standalone if needed
COPY cowbot_ws/src /ros2_ws/src/

# Build the workspace
RUN colcon build --symlink-install || true

# Source workspace in bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc

# Set up entrypoint script (will be created in container)
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

