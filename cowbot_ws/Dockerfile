FROM osrf/ros:jazzy-desktop-full

# Install Gazebo Harmonic and ROS-Gazebo bridge packages
RUN apt-get update && apt-get install -y \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-joint-state-publisher-gui \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace

# Source ROS setup in bashrc
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "if [ -f /workspace/install/setup.bash ]; then source /workspace/install/setup.bash; fi" >> ~/.bashrc

# Set environment variables for Gazebo
ENV GZ_SIM_RESOURCE_PATH=/workspace/src/cowbot_gazebo/models:/workspace/src/cowbot_gazebo/worlds
ENV GZ_SIM_SYSTEM_PLUGIN_PATH=/opt/ros/jazzy/lib

CMD ["/bin/bash"]
