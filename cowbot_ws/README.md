# Cowbot ROS 2 Workspace

This workspace contains the ROS 2 packages for the Cowbot autonomous robot, including simulation, navigation, sensor fusion, and hardware control.

## Overview

- **cowbot_description**: Robot URDF/Xacro models and visualization
- **cowbot_gazebo**: Gazebo Harmonic simulation launch files and worlds
- **cowbot_navigation**: Navigation, obstacle avoidance, and sensor fusion
- **cowbot_bringup**: Hardware bringup and sensor integration
- **serial_motor**: Serial communication with motor controllers
- **serial_motor_msgs**: Custom message definitions for motor control
- **Lslidar_ROS2_driver**: LSLidar N10 LiDAR driver for ROS 2

## System Requirements

### Native Installation (Ubuntu 24.04)
- **ROS 2 Jazzy** (installed and sourced)
- **Gazebo Harmonic** (gz-sim v8+)
- **RViz2** for visualization
- Python 3.12+ with OpenCV

### Hardware (Physical Robot)
- LSLidar N10 (270° LiDAR)
- USB Camera (Raspberry Pi camera or compatible)
- Arduino Nano (motor controller)
- Differential drive robot base

## Quick Start

### Simulation (No Hardware Required)

The simulation provides a complete virtual environment with working sensors and robot control.

#### 1. Install Dependencies

```bash
# Install Gazebo Harmonic and ROS packages
sudo apt update
sudo apt install -y \
    ros-jazzy-gz-sim-vendor \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-xacro \
    ros-jazzy-teleop-twist-keyboard
```

#### 2. Build the Workspace

```bash
cd ~/cowbot/cowbot_ws
colcon build --symlink-install
source install/setup.bash
```

#### 3. Launch Simulation

```bash
# Launch complete simulation (Gazebo + RViz)
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

This starts:
- ✅ Gazebo Harmonic with warehouse environment
- ✅ Cowbot robot with LiDAR and camera sensors
- ✅ RViz2 with sensor visualization
- ✅ All ROS-Gazebo bridges

#### 4. Control the Robot

In a **new terminal**:

```bash
source ~/cowbot/cowbot_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args --remap cmd_vel:=/cowbot/cmd_vel
```

Use keyboard to drive:
- `i` = forward, `k` = stop, `,` = backward
- `j` = left, `l` = right

### Hardware (Physical Robot)

#### 1. Install Dependencies

```bash
sudo apt update
sudo apt install -y \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport \
    ros-jazzy-v4l2-camera \
    ros-jazzy-sensor-msgs \
    ros-jazzy-geometry-msgs \
    ros-jazzy-nav-msgs \
    python3-opencv \
    python3-colcon-common-extensions
```

#### 2. Build the Workspace

```bash
cd ~/cowbot/cowbot_ws
rm -rf build/ install/ log/
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
```

#### 3. Launch Hardware with Sensor Fusion

**Terminal 1** - Hardware launch:
```bash
cd ~/cowbot/cowbot_ws
source install/setup.bash
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml
```

**Terminal 2** - Autonomous navigation:
```bash
cd ~/cowbot/cowbot_ws
source install/setup.bash
ros2 run cowbot_navigation robot_control
```

See main README for complete hardware usage documentation.

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
