# Docker Build Notes

## Package Changes in ROS 2 Jazzy

**Important:** In ROS 2 Jazzy, the Gazebo packages have changed:
- ❌ `ros-jazzy-gazebo-ros-pkgs` - **DOES NOT EXIST**
- ❌ `ros-jazzy-gazebo-ros2-control` - **DOES NOT EXIST**
- ✅ Use `gz-jazzy` instead (Ignition Gazebo)

## If Build Fails

1. **Check if Gazebo is already in base image:**
   ```bash
   docker run -it --rm osrf/ros:jazzy-desktop-full which gz
   ```

2. **If Gazebo exists, remove `gz-jazzy` from Dockerfile**

3. **See BUILD_TROUBLESHOOTING.md for more solutions**

## Current Dockerfile

The Dockerfile uses `gz-jazzy` for Gazebo. If this fails:
- Check BUILD_TROUBLESHOOTING.md
- Try removing gz-jazzy if base image already has Gazebo
- Check available packages: `apt-cache search gz-jazzy`

