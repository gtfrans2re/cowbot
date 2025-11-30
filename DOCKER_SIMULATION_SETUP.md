# Docker Simulation Setup Guide

## Overview

This guide explains how to run Gazebo simulation in Docker containers. This approach is useful when:
- You have a more powerful machine (not the 4GB RPi)
- You want isolated simulation environment
- You need consistent setup across different machines

## Prerequisites

- Docker installed on your machine
- At least 8GB RAM (16GB recommended)
- GPU support (optional but recommended for Gazebo)

## Option 1: Docker Compose (Recommended)

### Step 1: Create Docker Compose File

Create `~/cowbot/docker/docker-compose.yml`:

```yaml
version: '3.8'

services:
  gazebo:
    image: osrf/ros:jazzy-desktop-full
    container_name: cowbot_gazebo
    network_mode: host
    environment:
      - DISPLAY=${DISPLAY}
      - QT_X11_NO_MITSHM=1
      - ROS_DOMAIN_ID=0
      - ROS_LOCALHOST_ONLY=0
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
      - ./cowbot_ws:/ros2_ws/src/cowbot_ws:ro
      - gazebo_models:/root/.gazebo/models
      - gazebo_worlds:/root/.gazebo/worlds
    working_dir: /ros2_ws
    command: bash -c "colcon build --symlink-install && source install/setup.bash && ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
    stdin_open: true
    tty: true
    privileged: true

volumes:
  gazebo_models:
  gazebo_worlds:
```

### Step 2: Create Dockerfile (Alternative)

Create `~/cowbot/docker/simulation/Dockerfile`:

```dockerfile
FROM osrf/ros:jazzy-desktop-full

# Install dependencies
RUN apt-get update && apt-get install -y \
    ros-jazzy-gazebo-ros-pkgs \
    ros-jazzy-gazebo-ros2-control \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport \
    ros-jazzy-tf2-tools \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies if needed
RUN pip3 install --no-cache-dir \
    opencv-python-headless \
    numpy

# Set up workspace
WORKDIR /ros2_ws

# Copy workspace source
COPY cowbot_ws/src /ros2_ws/src/

# Build workspace
RUN colcon build --symlink-install

# Source workspace in bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc

# Default command
CMD ["bash"]
```

### Step 3: Build Docker Image

```bash
cd ~/cowbot/docker/simulation
docker build -t cowbot-simulation:latest .
```

### Step 4: Run Container

**With X11 forwarding (for GUI):**
```bash
xhost +local:docker
docker run -it --rm \
    --network host \
    --env DISPLAY=$DISPLAY \
    --env QT_X11_NO_MITSHM=1 \
    --env ROS_DOMAIN_ID=0 \
    --env ROS_LOCALHOST_ONLY=0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v ~/cowbot/cowbot_ws:/ros2_ws/src/cowbot_ws:ro \
    --privileged \
    cowbot-simulation:latest

# Inside container:
source install/setup.bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

**Headless mode (no GUI):**
```bash
docker run -it --rm \
    --network host \
    --env ROS_DOMAIN_ID=0 \
    --env ROS_LOCALHOST_ONLY=0 \
    -v ~/cowbot/cowbot_ws:/ros2_ws/src/cowbot_ws:ro \
    --privileged \
    cowbot-simulation:latest

# Inside container:
source install/setup.bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py headless:=true
```

## Option 2: Pre-built Docker Image with GPU Support

### NVIDIA Docker Setup (for GPU acceleration)

1. Install NVIDIA Docker runtime:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. Run with GPU:
```bash
docker run -it --rm \
    --gpus all \
    --network host \
    --env DISPLAY=$DISPLAY \
    --env QT_X11_NO_MITSHM=1 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v ~/cowbot/cowbot_ws:/ros2_ws/src/cowbot_ws:ro \
    --privileged \
    cowbot-simulation:latest
```

## Network Bridge from Docker Container

To bridge Docker container with RPi:

1. **Container must use host network mode:**
```yaml
network_mode: host
```

2. **Set ROS_DOMAIN_ID in container:**
```bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
```

3. **Verify connectivity:**
```bash
# Inside container
ros2 topic list
# Should see topics from RPi if both on same network
```

## Troubleshooting

### Problem: X11 display errors

**Solution:**
```bash
xhost +local:docker
export DISPLAY=$DISPLAY
```

### Problem: Container can't see RPi topics

**Solution:**
- Use `--network host` mode
- Ensure ROS_DOMAIN_ID matches on both
- Check firewall rules

### Problem: Gazebo is slow

**Solutions:**
- Use GPU acceleration (NVIDIA Docker)
- Increase container resources
- Run in headless mode and use RViz separately

### Problem: Models not loading

**Solution:**
- Mount model directory as volume
- Check GAZEBO_MODEL_PATH in container

## Advantages of Docker

✅ **Isolated Environment**: No conflicts with system packages
✅ **Reproducible**: Same setup every time
✅ **Portable**: Works on any machine with Docker
✅ **Easy Cleanup**: Remove container when done

## Disadvantages

❌ **Resource Overhead**: Docker adds ~200-500MB RAM overhead
❌ **X11 Complexity**: Display forwarding can be tricky
❌ **Network Setup**: Requires careful network configuration

## Recommendation

**For your use case (4GB RPi), I recommend:**
1. **Use local machine directly** (no Docker) - simpler setup
2. **Or use Docker on a more powerful machine** (8GB+ RAM)

Docker on RPi is **not recommended** due to resource constraints.

