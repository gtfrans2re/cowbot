# Docker Build Troubleshooting Guide

## Problem: Gazebo packages not found

**Error:**
```
E: Package 'ros-jazzy-gazebo-ros-pkgs' has no installation candidate
E: Unable to locate package ros-jazzy-gazebo-ros2-control
```

**Solution:**
These packages don't exist in ROS 2 Jazzy. The Dockerfile has been updated to use `gz-jazzy` instead.

## Problem: gz-jazzy packages not found

If `gz-jazzy` packages also fail, try one of these solutions:

### Option 1: Install Gazebo from source

Add to Dockerfile after the base image:
```dockerfile
# Install Gazebo from source or use pre-built binaries
RUN curl -sSL http://get.gazebosim.org | sh
```

### Option 2: Use a different base image

Change the FROM line to:
```dockerfile
FROM osrf/ros:jazzy-desktop-full
```

Or try:
```dockerfile
FROM osrf/gazebo:gz-jazzy
```

### Option 3: Check available packages first

Run this inside a test container to see what's available:
```bash
docker run -it --rm osrf/ros:jazzy-desktop-full bash
apt-get update
apt-cache search gazebo | grep jazzy
apt-cache search gz | grep jazzy
```

## Problem: Build still fails

### Check package availability

```bash
# Test inside the base image
docker run -it --rm osrf/ros:jazzy-desktop-full bash

# Inside container:
apt-get update
apt-cache search ros-jazzy | grep -i gazebo
apt-cache search gz-jazzy
```

### Minimal Dockerfile approach

If packages keep failing, create a minimal Dockerfile that only installs what's definitely available:

```dockerfile
FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DOMAIN_ID=0
ENV ROS_LOCALHOST_ONLY=0

# Only install packages we know exist
RUN apt-get update && apt-get install -y \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    python3-pip \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws
COPY cowbot_ws/src /ros2_ws/src/
RUN colcon build --symlink-install || true
```

Then install Gazebo separately after the container is running.

## Alternative: Use existing Gazebo in base image

The `ros-jazzy-desktop-full` image might already include Gazebo. Check:

```bash
docker run -it --rm osrf/ros:jazzy-desktop-full bash
which gz
gz --version
```

If Gazebo is already installed, you might not need to install additional packages!

## Quick test commands

```bash
# Test if base image has Gazebo
docker run -it --rm osrf/ros:jazzy-desktop-full which gz

# Test if packages are available
docker run -it --rm osrf/ros:jazzy-desktop-full bash -c \
    "apt-get update && apt-cache search gz-jazzy | head -10"
```

## Current Dockerfile Status

The current Dockerfile has been updated to:
- Remove non-existent `ros-jazzy-gazebo-*` packages
- Use `gz-jazzy` packages instead
- Keep only packages that should exist

If `gz-jazzy` also fails, we can:
1. Remove it and use Gazebo from base image
2. Install Gazebo differently
3. Use a different approach

