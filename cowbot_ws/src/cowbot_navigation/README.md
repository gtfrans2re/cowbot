# Cowbot Navigation

LiDAR-based obstacle detection and avoidance system for Cowbot.

## Overview

This package provides obstacle detection and avoidance capabilities using LiDAR data. It includes:

- **robot_interface**: ROS2 node that bridges LiDAR scan data, odometry, IMU, and cmd_vel
- **robot_control**: Autonomous navigation with sensor fusion (camera + LiDAR)
- **camera_obstacle_detector**: Camera-based obstacle detection node
- **Bash scripts**: Simple patrol and statistics monitoring

## Package Structure

```
cowbot_navigation/
├── cowbot_navigation/
│   ├── robot_interface.py              # Main interface node
│   ├── robot_control_client.py         # Main control with sensor fusion
│   ├── robot_control_debug.py          # Debug version with detailed logging
│   ├── camera_obstacle_detector.py     # Camera obstacle detection
│   ├── robot_control_classed.py        # Legacy: OOP implementation
│   └── robot_control_noclass.py        # Legacy: Procedural implementation
├── scripts/
│   ├── robot_functions.bash            # Bash helper functions
│   └── robot_statistics.bash           # Telemetry monitoring
└── launch/
    ├── robot_interface.launch.py       # Robot interface launch file
    └── sensor_fusion.launch.py         # Complete sensor fusion system
```

## Installation

1. Build the package:
```bash
cd ~/cowbot_ws
colcon build --packages-select cowbot_navigation --symlink-install
source install/setup.bash
```

## Usage

### 1. Start the Robot Interface

The robot_interface node must be running for all control methods:

```bash
ros2 launch cowbot_navigation robot_interface.launch.py
```

Or run it directly:
```bash
ros2 run cowbot_navigation robot_interface
```

### 2. Control Methods

#### Python - Autonomous Navigation with Sensor Fusion (Recommended)
```bash
ros2 run cowbot_navigation robot_control
```

#### Python - Debug Version
```bash
ros2 run cowbot_navigation robot_control_debug
```

#### Bash - Simple Patrol
```bash
cd ~/cowbot_ws/src/cowbot_navigation/scripts
./robot_functions.bash
```

#### Bash - Statistics Monitor
```bash
cd ~/cowbot_ws/src/cowbot_navigation/scripts
./robot_statistics.bash
```

## Topics

### Subscribed Topics
- `/scan` (sensor_msgs/LaserScan) - LiDAR scan data
- `/odom` (nav_msgs/Odometry) - Odometry data
- `/imu` (sensor_msgs/Imu) - IMU data

### Published Topics
- `/cmd_vel` (geometry_msgs/Twist) - Velocity commands

## Parameters

The robot_interface node exposes these parameters for easy access:

### Velocity Control
- `cmd_vel_linear` - Linear velocity (m/s)
- `cmd_vel_angular` - Angular velocity (rad/s)

### Scan Ranges
- `scan_front_ray_range` - Minimum distance in front sector
- `scan_front_left_ray_range` - Minimum distance in front-left sector
- `scan_front_right_ray_range` - Minimum distance in front-right sector
- `scan_left_ray_range` - Minimum distance in left sector
- `scan_right_ray_range` - Minimum distance in right sector

### Odometry
- `odom_distance` - Total distance traveled (m)
- `odom_direction` - Cardinal direction (N, NE, E, SE, S, SW, W, NW)
- `odom_position_x`, `odom_position_y`, `odom_position_z` - Position
- `odom_orientation_r`, `odom_orientation_p`, `odom_orientation_y` - Orientation (roll, pitch, yaw)

### IMU
- `imu_angular_velocity_x`, `imu_angular_velocity_y`, `imu_angular_velocity_z`
- `imu_linear_acceleration_x`, `imu_linear_acceleration_y`, `imu_linear_acceleration_z`

## Obstacle Avoidance Algorithm

The enhanced obstacle avoidance algorithm:

1. **Forward motion**: Robot moves forward if front sector is clear (> threshold)
2. **Obstacle detection**: When obstacle detected, robot stops
3. **Direction evaluation**: Checks all sectors (front-left, front-right, left, right)
4. **Best path selection**: Chooses direction with maximum clearance
5. **Turning**: Rotates until front sector clears
6. **Resume**: Returns to forward motion

## Configuration

Edit the following parameters in the control scripts to tune behavior:

- `forward_speed`: Linear velocity when moving forward (default: 0.08 m/s)
- `turn_speed`: Angular velocity when turning (default: 0.15 rad/s)
- `threshold`: Minimum safe distance (default: 0.6 m)

Note: Legacy implementations (robot_control_classed.py, robot_control_noclass.py) are available but not registered as entry points. Use `robot_control` for the latest sensor fusion-enabled navigation.

## Integration with Existing System

To integrate with your existing bringup:

1. Add robot_interface to your main launch file:
```python
from launch_ros.actions import Node

# In your launch description:
Node(
    package='cowbot_navigation',
    executable='robot_interface',
    name='robot_interface',
    output='screen',
),
```

2. Or include the launch file:
```python
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        PathJoinSubstitution([
            FindPackageShare('cowbot_navigation'),
            'launch',
            'robot_interface.launch.py'
        ])
    ])
)
```

## Troubleshooting

### No scan data
Check if LiDAR driver is running:
```bash
ros2 topic list | grep scan
ros2 topic echo /scan
```

### Robot not moving
Verify robot_interface is running and publishing:
```bash
ros2 topic echo /cmd_vel
```

Check parameter values:
```bash
ros2 param get /robot_interface cmd_vel_linear
ros2 param get /robot_interface cmd_vel_angular
```

### Bash scripts not working
Ensure robot_interface node is running first, and check parameters:
```bash
ros2 param list | grep robot_interface
```

## License

MIT
