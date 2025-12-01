# Cowbot ROS 2 Workspace

This workspace contains the ROS 2 packages for the Cowbot robot, including simulation, navigation, and hardware control.

## Overview

- **cowbot_description**: Robot URDF/Xacro models and visualization
- **cowbot_gazebo**: Gazebo simulation launch files and worlds
- **cowbot_navigation**: Navigation and obstacle avoidance logic
- **cowbot_bringup**: Hardware bringup and sensor fusion
- **serial_motor**: Serial communication with motor controllers
- **serial_motor_msgs**: Custom message definitions for motor control

## System Requirements

### Native Installation (Ubuntu 24.04)
- ROS 2 Jazzy
- Note: Gazebo Classic is not available on Ubuntu 24.04

### Docker Installation (Recommended for Simulation)
- Docker and Docker Compose
- Ubuntu 24.04 (host)
- X11 display server

## Quick Start

### Using Docker (Simulation)

The Docker setup provides a complete ROS 2 Jazzy environment with Gazebo Harmonic for simulation.

#### 1. Build the Docker Image

```bash
cd ~/cowbot/cowbot_ws
sudo docker build -t cowbot_gazebo:latest .
```

#### 2. Run the Simulation

```bash
./run_docker_sim.sh
```

This will:
- Set up X11 authentication for GUI display
- Build the workspace inside the container
- Launch Gazebo Harmonic with the warehouse world
- Spawn the cowbot robot
- Start RViz2 for visualization

#### 3. Interactive Docker Shell

For development and debugging:

```bash
./run_docker_shell.sh
```

Inside the container:
```bash
# Build the workspace
colcon build

# Source the workspace
source install/setup.bash

# Launch components individually
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

### Native Installation (Hardware/Development)

#### 1. Install Dependencies

```bash
sudo apt update
sudo apt install -y \
    ros-jazzy-joint-state-publisher-gui \
    python3-colcon-common-extensions
```

#### 2. Build the Workspace

```bash
cd ~/cowbot/cowbot_ws
rm -rf build/ install/ log/
source /opt/ros/jazzy/setup.bash
colcon build
```

#### 3. Launch

```bash
source install/setup.bash

# For hardware
ros2 launch cowbot_bringup hardware.launch.py

# For development
ros2 launch cowbot_description display.launch.py
```

## Docker Architecture

The Docker setup includes:

- **Base Image**: `osrf/ros:jazzy-desktop-full`
- **Gazebo**: Gazebo Harmonic (gz-sim)
- **ROS-Gazebo Bridge**: `ros-jazzy-ros-gz-sim` and `ros-jazzy-ros-gz-bridge`
- **Workspace**: Mounted from host at `/workspace`

### Key Changes from Gazebo Classic

The simulation has been migrated from Gazebo Classic (gazebo11) to Gazebo Harmonic:

- **Launch files**: Updated to use `gz sim` instead of `gzserver/gzclient`
- **Spawning**: Using `ros_gz_sim` instead of `gazebo_ros`
- **Bridge**: ROS-Gazebo bridge for topic communication
- **Environment variables**: `GZ_SIM_RESOURCE_PATH` instead of `GAZEBO_MODEL_PATH`

## Known Issues

### Simulation Issues
1. **World file compatibility**: The `.world` files may need conversion from Gazebo Classic format to SDF format for Gazebo Harmonic
2. **Model paths**: Some models may not load if they reference Gazebo Classic paths
3. **Plugin compatibility**: Gazebo Classic plugins need to be replaced with Gazebo Harmonic equivalents

### Workarounds
- The simulation currently uses compatibility mode
- Some features may require additional ROS-Gazebo bridge configuration

## Troubleshooting

### Docker X11 Permission Denied

```bash
xhost +local:docker
```

### Build Artifacts Conflict

If you get CMake cache errors:

```bash
rm -rf build/ install/ log/
```

### Container Doesn't Start

Check Docker permissions:

```bash
sudo usermod -aG docker $USER
# Log out and back in
```

## Development Workflow

### Edit Code on Host, Run in Docker

1. Edit files in `~/cowbot/cowbot_ws/src/` on your host machine
2. The workspace is mounted in the container, so changes are immediately visible
3. Rebuild inside the container or restart the simulation

### Using Interactive Shell

```bash
./run_docker_shell.sh

# Inside container
colcon build --packages-select cowbot_navigation
source install/setup.bash
ros2 run cowbot_navigation robot_control_client
```

## Additional Resources

- [ROS 2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic)
- [ros_gz Bridge](https://github.com/gazebosim/ros_gz)

## License

[Your License Here]

## Contributors

[Your Contributors Here]
