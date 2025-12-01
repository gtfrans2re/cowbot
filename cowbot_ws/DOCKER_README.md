# Cowbot Docker Setup

This document provides detailed information about running Cowbot simulation using Docker with Gazebo Harmonic.

## Overview

Due to Ubuntu 24.04 not supporting Gazebo Classic (gazebo11), we use Docker to provide a complete ROS 2 Jazzy environment with Gazebo Harmonic for simulation.

## Prerequisites

- Docker installed on Ubuntu 24.04
- X11 display server (for GUI)
- Docker Compose (optional, for easier orchestration)

### Install Docker

```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# Add user to docker group (to avoid using sudo)
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
```

## Files

- `Dockerfile` - Docker image definition with ROS 2 Jazzy and Gazebo Harmonic
- `docker-compose.yml` - Docker Compose configuration for easy launching
- `run_docker_sim.sh` - Helper script to run simulation with X11 support
- `run_docker_shell.sh` - Helper script to run interactive shell

## Docker Image

### Base Image
- `osrf/ros:jazzy-desktop-full` - Official ROS 2 Jazzy Docker image

### Installed Packages
- `ros-jazzy-ros-gz-sim` - Gazebo Harmonic simulator integration
- `ros-jazzy-ros-gz-bridge` - ROS-Gazebo topic bridge
- `ros-jazzy-joint-state-publisher-gui` - Joint state control GUI
- `python3-colcon-common-extensions` - Build tools

### Environment Variables
- `GZ_SIM_RESOURCE_PATH` - Path to Gazebo models and worlds
- `GZ_SIM_SYSTEM_PLUGIN_PATH` - Path to Gazebo plugins

## Building the Image

### Method 1: Using Docker Build

```bash
cd ~/cowbot/cowbot_ws
sudo docker build -t cowbot_gazebo:latest .
```

Build time: ~2-3 minutes (depending on network speed)

### Method 2: Using Docker Compose

```bash
cd ~/cowbot/cowbot_ws
sudo docker-compose build
```

## Running the Simulation

### Method 1: Using Helper Script (Recommended)

```bash
./run_docker_sim.sh
```

This script:
1. Sets up X11 authentication (`/tmp/.docker.xauth`)
2. Allows Docker to connect to X server (`xhost +local:docker`)
3. Runs `docker-compose up --build`
4. Cleans up X11 permissions after exit

### Method 2: Using Docker Compose Directly

```bash
# Set up X11
xhost +local:docker
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
chmod 644 $XAUTH

# Run simulation
sudo docker-compose up

# Cleanup
xhost -local:docker
```

### Method 3: Manual Docker Run

```bash
# Set up X11 (same as above)
xhost +local:docker

# Run container
sudo docker run -it --rm \
    --name cowbot_sim \
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
    /bin/bash -c "rm -rf build install log && \
                  source /opt/ros/jazzy/setup.bash && \
                  colcon build && \
                  source install/setup.bash && \
                  ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"

# Cleanup
xhost -local:docker
```

## Interactive Development

### Starting Interactive Shell

```bash
./run_docker_shell.sh
```

Or manually:

```bash
xhost +local:docker
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
```

### Inside the Container

```bash
# Build workspace
colcon build

# Build specific packages
colcon build --packages-select cowbot_navigation

# Source workspace
source install/setup.bash

# Launch simulation
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py

# Launch specific components
ros2 launch cowbot_gazebo botbox_world.launch.xml
ros2 launch cowbot_description display.launch.py

# Run individual nodes
ros2 run rviz2 rviz2
ros2 run cowbot_navigation robot_control_client
```

## Docker Configuration Details

### Volumes Mounted

1. **Workspace**: `~/cowbot/cowbot_ws` → `/workspace`
   - Your source code is mounted, so edits on host are immediately visible in container

2. **X11 Socket**: `/tmp/.X11-unix` → `/tmp/.X11-unix`
   - Allows GUI applications (Gazebo, RViz) to display on host

3. **X11 Auth**: `/tmp/.docker.xauth` → `/tmp/.docker.xauth`
   - X11 authentication for display access

4. **GPU Device**: `/dev/dri` → `/dev/dri`
   - GPU acceleration for Gazebo rendering

### Network Mode

- `host` - Container uses host network stack for ROS 2 discovery

### Privileges

- `privileged: true` - Required for GPU access and some device interactions

## Gazebo Harmonic Migration

### Changes from Gazebo Classic

| Aspect | Gazebo Classic | Gazebo Harmonic |
|--------|---------------|-----------------|
| Executable | `gzserver`, `gzclient` | `gz sim` |
| Launch | `gazebo_ros` | `ros_gz_sim` |
| Spawning | `gazebo_ros/spawn_entity.py` | `ros_gz_sim/create` |
| Bridge | Built-in | `ros_gz_bridge` |
| Model Path | `GAZEBO_MODEL_PATH` | `GZ_SIM_RESOURCE_PATH` |
| World Format | `.world` (SDF 1.4-1.6) | `.sdf` (SDF 1.8+) |

### Modified Files

- `src/cowbot_gazebo/launch/botbox_world.launch.xml` - Updated to use `gz sim`
- `src/cowbot_gazebo/launch/spawn_in_gazebo.launch.py` - Updated to use `ros_gz_sim`
- `src/cowbot_gazebo/config/ros_gz_bridge.yaml` - ROS-Gazebo topic bridge configuration
- `src/cowbot_gazebo/CMakeLists.txt` - Added config directory to install

## Troubleshooting

### Issue: X11 Permission Denied

**Symptoms**: GUI windows don't appear, errors about DISPLAY

**Solution**:
```bash
xhost +local:docker
```

**Permanent Solution** (less secure):
```bash
# Add to ~/.bashrc
xhost +local:docker > /dev/null 2>&1
```

### Issue: GPU/Graphics Performance

**Symptoms**: Slow rendering, low FPS in Gazebo

**Solutions**:
1. Ensure `/dev/dri` is mounted
2. Check GPU drivers on host:
   ```bash
   nvidia-smi  # For NVIDIA
   glxinfo | grep "OpenGL"  # For any GPU
   ```
3. For NVIDIA GPUs, consider using nvidia-docker

### Issue: Build Cache Conflicts

**Symptoms**: CMake errors about different source directories

**Solution**:
```bash
# On host
rm -rf build/ install/ log/

# Or in docker-compose.yml, we already clean before build
```

### Issue: World/Models Not Loading

**Symptoms**: Gazebo starts but world is empty, models missing

**Cause**: World files use Gazebo Classic format, incompatible with Harmonic

**Solution**: Convert world files to SDF 1.8+ format
```bash
# Inside container
gz sdf --check /workspace/src/cowbot_gazebo/worlds/botbox_warehouse.world
```

### Issue: Robot Not Spawning

**Symptoms**: Gazebo loads but robot doesn't appear

**Possible Causes**:
1. URDF parsing errors
2. ros_gz_sim create service not available
3. Topic name mismatch

**Debug**:
```bash
# Check robot description
ros2 topic echo /cowbot_robot_description

# Check Gazebo services
ros2 service list | grep gz

# Check logs
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py --show-args
```

### Issue: Container Exits Immediately

**Symptoms**: Container starts and stops

**Solution**: Check logs
```bash
sudo docker-compose logs
# or
sudo docker logs cowbot_simulation
```

### Issue: ROS 2 Topics Not Visible

**Symptoms**: `ros2 topic list` shows no Gazebo topics

**Cause**: ros_gz_bridge not running or misconfigured

**Solution**:
1. Check bridge configuration: `src/cowbot_gazebo/config/ros_gz_bridge.yaml`
2. Verify bridge is running:
   ```bash
   ros2 node list | grep bridge
   ```
3. Check bridge topics:
   ```bash
   ros2 topic list | grep gz
   ```

## Performance Tips

### Reducing Build Time

1. **Use Docker layer caching**:
   - Don't change Dockerfile frequently
   - Build image once, reuse many times

2. **Incremental builds**:
   ```bash
   # Inside container, only rebuild changed packages
   colcon build --packages-select cowbot_navigation
   ```

3. **Pre-built image**:
   - Save built image to avoid rebuilding
   ```bash
   sudo docker save cowbot_gazebo:latest | gzip > cowbot_gazebo.tar.gz
   # Later restore:
   gunzip -c cowbot_gazebo.tar.gz | sudo docker load
   ```

### Reducing Simulation Lag

1. **Reduce physics rate** in world file
2. **Disable shadows** in Gazebo GUI
3. **Use simpler models** for testing
4. **Close RViz** if not needed

## Development Workflow

### Typical Development Cycle

1. **Edit code on host**:
   ```bash
   # On host
   vim ~/cowbot/cowbot_ws/src/cowbot_navigation/cowbot_navigation/robot_control_client.py
   ```

2. **Rebuild in container**:
   ```bash
   # In container shell
   colcon build --packages-select cowbot_navigation
   source install/setup.bash
   ```

3. **Test changes**:
   ```bash
   # In container
   ros2 run cowbot_navigation robot_control_client
   ```

4. **Iterate** (repeat steps 1-3)

### Using Multiple Terminals

**Terminal 1** - Run simulation:
```bash
./run_docker_sim.sh
```

**Terminal 2** - Interactive shell:
```bash
sudo docker exec -it cowbot_simulation bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
# Run commands
```

**Terminal 3** - Monitor topics:
```bash
sudo docker exec -it cowbot_simulation bash
source /opt/ros/jazzy/setup.bash
ros2 topic list
ros2 topic echo /scan
```

## Next Steps

### TODO: Fix World File Compatibility

The current `.world` files are in Gazebo Classic format. To fully support Gazebo Harmonic:

1. Convert world files to SDF 1.8+
2. Update model references
3. Replace Classic plugins with Harmonic equivalents
4. Test robot spawning and sensors

### TODO: Optimize ROS-Gazebo Bridge

Currently only bridging clock. Add more topics as needed:
- Camera images
- Laser scans
- IMU data
- Joint states
- etc.

Edit `src/cowbot_gazebo/config/ros_gz_bridge.yaml` to add topics.

## Additional Resources

- [Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic)
- [ros_gz GitHub](https://github.com/gazebosim/ros_gz)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [ROS 2 Jazzy Docs](https://docs.ros.org/en/jazzy/)

## Support

For issues specific to this Docker setup, check:
1. Docker logs: `sudo docker-compose logs`
2. Container shell: `./run_docker_shell.sh`
3. Host system requirements (X11, GPU drivers)

For ROS 2 or Gazebo issues, consult official documentation.
