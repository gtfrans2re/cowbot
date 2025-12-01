# Cowbot - Autonomous Robotic System for Animal Welfare Monitoring

An autonomous robotic system built on ROS 2 Jazzy, featuring advanced camera-LiDAR sensor fusion for robust obstacle detection and navigation.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Remote Access & Networking](#remote-access--networking)
- [Usage](#usage)
- [Sensor Fusion System](#sensor-fusion-system)
- [Navigation Package](#navigation-package)
- [Configuration & Tuning](#configuration--tuning)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview

Cowbot is an autonomous robot designed for animal welfare monitoring. The system uses advanced sensor fusion combining LiDAR and camera sensors to provide robust obstacle detection and navigation capabilities. Key features include:

- **Dual Sensor Fusion**: Combines LiDAR (accurate distance) and Camera (visual detection) for superior obstacle detection
- **Enhanced Navigation**: Multi-criteria decision making with sensor confidence scoring
- **8-Direction Awareness**: Full 360° obstacle detection and avoidance
- **Temporal Filtering**: Stable, noise-reduced sensor readings
- **Safety First**: Conservative fusion strategy and motor enable/disable controls

---

## Features

### Sensor Fusion
- **LiDAR Integration**: LSLidar N10 support with 270° coverage, 0.05-20m range
- **Camera Integration**: Real-time vision processing with edge/contour detection
- **Intelligent Fusion**: Weighted average when sensors agree, conservative minimum when they disagree
- **Confidence Scoring**: Sensor agreement metrics (0-1) for decision quality assessment
- **Temporal Filtering**: 3-frame history smoothing for stable readings

### Navigation
- **Autonomous Obstacle Avoidance**: Multi-criteria scoring for optimal path selection
- **8-Direction Detection**: Front, front-left, front-right, left, right, back, back-left, back-right
- **Enhanced Decision Making**: Non-linear scoring with forward preference and safety penalties
- **Smooth Operation**: Velocity smoothing and intelligent maneuver selection

### Safety
- **Motor Enable/Disable**: Safety gate to prevent accidental movement
- **Conservative Approach**: Uses minimum range when sensors disagree
- **Emergency Stop**: Immediate halt capability
- **Validation**: All sensor readings validated and clamped to safe ranges

---

## Quick Start

### Prerequisites

1. **Hardware Connected**:
   - LiDAR (LSLidar N10) connected and powered
   - Camera connected (Raspberry Pi camera or USB camera)
   - Motors/Arduino Nano connected
   - All hardware powered on

2. **Software**:
   - ROS 2 Jazzy installed
   - Workspace dependencies built

### Build the Workspace

```bash
cd ~/cowbot_ws
colcon build --symlink-install
source install/setup.bash
```

**Important**: You must source the workspace in **each terminal** you open:
```bash
cd ~/cowbot_ws
source install/setup.bash
```

### Launch the System

**Terminal 1** - Launch hardware with sensor fusion:
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml
```

Wait for initialization (10-15 seconds). You should see:
- `RobotInterface node initialized with sensor fusion`
- `Camera obstacle detector initialized`

**Terminal 2** - Start autonomous navigation:
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 run cowbot_navigation robot_control
```

The robot will:
1. Run system tests (movement verification)
2. Enable motors (safety check)
3. Start autonomous navigation with sensor fusion

---

## Hardware Requirements

### Required Hardware

- **LiDAR**: LSLidar N10 (270° coverage, 0.05-20m range)
- **Camera**: Raspberry Pi camera or USB camera (800x600 recommended)
- **Motor Controller**: Arduino Nano with serial motor driver
- **IMU**: For orientation data
- **Wheel Encoders**: For odometry

### Hardware Connections

- LiDAR: USB connection (check `/dev/ttyUSB*`)
- Camera: Raspberry Pi camera port or USB (`/dev/video0` or `/dev/video1`)
- Arduino: Serial connection (`/dev/arduino_nano` or `/dev/ttyACM0`)
- Power: All components properly powered

### Verify Hardware

```bash
# Check camera
ls -l /dev/video*

# Check serial ports
ls -l /dev/ttyUSB* /dev/ttyACM*

# Check LiDAR (should publish /scan topic)
ros2 topic hz /scan
```

---

## Installation

### 1. Clone the Repository

```bash
cd ~
git clone <repository-url> cowbot
cd cowbot/cowbot_ws
```

### 2. Install Dependencies

```bash
# ROS 2 dependencies
sudo apt update
sudo apt install -y \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport \
    ros-jazzy-sensor-msgs \
    ros-jazzy-geometry-msgs \
    ros-jazzy-nav-msgs

# OpenCV (if not already installed)
sudo apt install -y python3-opencv

# v4l2 camera driver
sudo apt install -y ros-jazzy-v4l2-camera
```

### 3. Build Workspace

```bash
cd ~/cowbot_ws
colcon build --symlink-install
source install/setup.bash
```

### 4. Verify Installation

```bash
# Check packages are available
ros2 pkg list | grep -E "(cowbot|lslidar)"

# Check executables
ros2 pkg executables cowbot_navigation
```

Should show:
- `robot_interface`
- `robot_control`
- `robot_control_debug`
- `camera_obstacle_detector`

---

## Remote Access & Networking

### Overview

The cowbot can be accessed remotely via SSH and HTTP for development, monitoring, and control. Since enterprise networks like eduroam often have **client isolation** enabled (preventing devices from communicating directly), we use **Tailscale** - a mesh VPN that creates persistent connections between devices regardless of the underlying network.

### Why Tailscale?

✅ **Works on any network**: Bypasses client isolation, NAT, and firewalls
✅ **Persistent IPs**: Each device gets a permanent 100.x.x.x IP address
✅ **Zero configuration**: Automatic peer discovery and connection
✅ **Secure**: End-to-end encrypted connections
✅ **Free**: Free for personal use with up to 100 devices

### Finding Cowbot IP on Different Networks

#### On Your Personal Hotspot

When connected to your personal hotspot, the cowbot is typically discoverable via network scanning:

```bash
# Find your network gateway
ip route | grep default

# Scan the network (e.g., for 172.20.10.0/24)
sudo apt install -y nmap
nmap -sn 172.20.10.0/24

# Check devices with SSH/HTTP open
nmap -p 22,80 <IP_ADDRESS>
```

#### On Enterprise Networks (eduroam)

**Problem**: Enterprise networks use client isolation, which prevents direct device-to-device communication. Standard network scanning won't work.

**Solution**: Use Tailscale (see setup below) to create a direct encrypted tunnel between devices.

### Tailscale Setup (Recommended)

#### Step 1: Install Tailscale on Your Laptop

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Connect to Tailscale network
sudo tailscale up
```

This will provide a URL to authenticate. Open the URL in your browser, log in with your account (Google, Microsoft, GitHub, etc.), and approve the device.

```bash
# Verify connection and get your laptop's Tailscale IP
tailscale status
```

Your laptop will get a Tailscale IP like `100.x.x.x`.

#### Step 2: Install Tailscale on the Cowbot

**Connect to the cowbot via your hotspot first**, then run:

```bash
# SSH into cowbot via hotspot
ssh cowbot@<HOTSPOT_IP>

# Install Tailscale on cowbot
curl -fsSL https://tailscale.com/install.sh | sh

# Connect cowbot to Tailscale
sudo tailscale up
```

Open the authentication URL in your browser and approve the cowbot device.

```bash
# Verify cowbot is connected
tailscale status
```

The cowbot will get its own Tailscale IP like `100.x.x.x`.

#### Step 3: Access Cowbot via Tailscale

**From your laptop**, list all connected Tailscale devices:

```bash
tailscale status
```

You'll see both your laptop and the cowbot listed with their Tailscale IPs.

**SSH to cowbot using its Tailscale IP:**

```bash
# Example (use your actual cowbot Tailscale IP)
ssh cowbot@100.116.35.41
```

**Access cowbot web interface:**

```bash
# Example (use your actual cowbot Tailscale IP)
http://100.116.35.41
```

✅ **This works on ANY network** - your hotspot, eduroam, home WiFi, cellular, etc.!

### Network Configuration on Cowbot

#### Firewall Configuration

If you need to configure the cowbot's firewall to allow specific networks:

```bash
# Check firewall status
sudo ufw status

# Allow connections from a specific network (e.g., eduroam)
sudo ufw allow from 172.29.0.0/16

# Enable firewall if not already enabled
sudo ufw enable

# Verify rules
sudo ufw status numbered
```

**Note**: With Tailscale, firewall rules are less critical since Tailscale creates encrypted tunnels that bypass local network restrictions.

#### SSH Configuration

The SSH daemon should already be configured to accept connections:

```bash
# Check SSH service status
sudo systemctl status ssh

# Start SSH if not running
sudo systemctl start ssh

# Enable SSH to start on boot
sudo systemctl enable ssh

# Check SSH configuration
sudo cat /etc/ssh/sshd_config | grep -v "^#" | grep -v "^$"
```

### Troubleshooting Network Access

#### Cannot Find Cowbot on Local Network

**Problem**: Network scanning doesn't detect the cowbot.

**Solutions**:
1. **Use Tailscale** (recommended) - bypasses all network restrictions
2. Check if cowbot is on the correct network:
   ```bash
   # On cowbot
   ip addr show
   hostname -I
   ```
3. Verify both devices are on the same subnet
4. Check for client isolation on the network

#### SSH Connection Refused or Closed

**Problem**: `Connection closed by X.X.X.X port 22` or `Connection refused`

**Solutions**:
1. **Use Tailscale IP instead of local IP**
2. Verify SSH service is running:
   ```bash
   sudo systemctl status ssh
   sudo systemctl start ssh
   ```
3. Check firewall rules:
   ```bash
   sudo ufw status
   sudo ufw allow from <YOUR_IP>
   ```
4. Check SSH logs for errors:
   ```bash
   sudo journalctl -u ssh -n 50 --no-pager
   ```

#### Tailscale Not Connecting

**Problem**: Devices show as "offline" in Tailscale status.

**Solutions**:
1. Verify internet connectivity on both devices
2. Restart Tailscale:
   ```bash
   sudo systemctl restart tailscaled
   sudo tailscale up
   ```
3. Check Tailscale status:
   ```bash
   tailscale status
   tailscale ping <device-name>
   ```
4. Verify devices are authenticated in the Tailscale admin console:
   https://login.tailscale.com/admin/machines

#### Network Discovery Tools

Useful tools for network troubleshooting:

```bash
# Install network scanning tools
sudo apt install -y nmap arp-scan avahi-utils

# Scan local network
sudo arp-scan -l --interface=wlan0

# Check for mDNS broadcasts
avahi-browse -art

# Check ARP cache
ip neigh

# Scan specific IP for open ports
nmap -p 22,80,443 <IP_ADDRESS>
```

### Best Practices

1. **Always use Tailscale for remote access** - it's more reliable and secure than exposing services directly
2. **Keep Tailscale running on boot** - it's already configured as a systemd service
3. **Use Tailscale IPs in scripts and configurations** - they persist across network changes
4. **Monitor Tailscale connection** - check `tailscale status` if experiencing issues
5. **Keep both devices authenticated** - Tailscale keys expire after some time, re-authenticate if needed

---

## Usage

### Complete System Launch

**Terminal 1** - Hardware launch:
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml
```

**Terminal 2** - Autonomous navigation:
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 run cowbot_navigation robot_control
```

### Manual Control (Optional)

For manual testing before autonomous mode:

**Terminal 1** - Hardware launch (same as above)

**Terminal 2** - Keyboard teleop:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r /cmd_vel:=/cowbot/cmd_vel
```

### Monitoring Sensor Fusion

**Terminal 3** - Monitor sensor data:
```bash
# Real-time fused ranges
watch -n 0.5 'ros2 param get /robot_interface fused_front_range'

# Sensor agreement scores
ros2 param get /robot_interface sensor_agreement_front

# List all fused parameters
ros2 param list | grep fused
```

### Visual Monitoring

```bash
# View camera feed
ros2 run rqt_image_view rqt_image_view /camera/image_raw

# Check topic rates
ros2 topic hz /scan
ros2 topic hz /camera/image_raw
ros2 topic hz /camera/obstacle_ranges
```

---

## Sensor Fusion System

### Architecture

The sensor fusion system consists of three main components:

1. **Camera Obstacle Detector** (`camera_obstacle_detector.py`)
   - Processes camera images using OpenCV
   - Edge detection and contour analysis
   - Distance estimation based on area, height, and position
   - Publishes obstacle ranges to `/camera/obstacle_ranges`

2. **Robot Interface** (`robot_interface.py`)
   - Subscribes to LiDAR (`/scan`) and Camera (`/camera/obstacle_ranges`)
   - Fuses sensor data with temporal filtering
   - Calculates sensor agreement scores
   - Publishes fused ranges as ROS parameters

3. **Robot Control** (`robot_control_client.py`)
   - Uses fused sensor data for navigation decisions
   - Multi-criteria scoring algorithm
   - Enhanced obstacle avoidance with 8-direction awareness

### Fusion Algorithm

The fusion algorithm uses a conservative approach:

- **Sensor Agreement** (< 0.25m difference):
  - Uses weighted average: 65% LiDAR + 35% Camera
  - High confidence (agreement score > 0.7)

- **Sensor Disagreement** (≥ 0.25m difference):
  - Uses minimum range (conservative safety approach)
  - Lower confidence (agreement score decreases)

- **Single Sensor**:
  - Falls back to available sensor
  - Reduced confidence (0.6 for LiDAR-only, 0.4 for Camera-only)

### Sensor Sectors

Both sensors divide the field of view into 5 sectors:

| Sector | Angle | Description |
|--------|-------|-------------|
| Right | -90° | Right side |
| Front-Right | -45° | Front-right diagonal |
| Front | 0° | Straight ahead |
| Front-Left | 45° | Front-left diagonal |
| Left | 90° | Left side |

Back sectors (back, back-left, back-right) use LiDAR only.

### Enhanced Features

- **Temporal Filtering**: 3-frame history with median smoothing for stable readings
- **Range Validation**: All ranges clamped to 0.05m - 20.0m
- **Timeout Detection**: Camera data marked stale after 2 seconds
- **Improved Agreement Scoring**: Relative difference-based confidence metrics

---

## Navigation Package

### Package Structure

```
cowbot_navigation/
├── cowbot_navigation/
│   ├── robot_interface.py              # Main interface with sensor fusion
│   ├── robot_control_client.py         # Autonomous navigation (recommended)
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

### Available Executables

- `robot_interface`: Main sensor fusion bridge node
- `robot_control`: Autonomous navigation with sensor fusion (recommended)
- `robot_control_debug`: Debug version with detailed logging
- `camera_obstacle_detector`: Camera-based obstacle detection node

### ROS Topics

#### Subscribed Topics
- `/scan` (sensor_msgs/LaserScan) - LiDAR scan data
- `/camera/image_raw` (sensor_msgs/Image) - Camera image feed
- `/odom` (nav_msgs/Odometry) - Odometry data
- `/imu` (sensor_msgs/Imu) - IMU data

#### Published Topics
- `/camera/obstacle_ranges` (std_msgs/Float32MultiArray) - Camera-detected ranges
- `/cowbot/cmd_vel` (geometry_msgs/Twist) - Velocity commands

### ROS Parameters

The `robot_interface` node exposes many parameters for monitoring and control:

**Velocity Control:**
- `cmd_vel_linear` - Linear velocity (m/s)
- `cmd_vel_angular` - Angular velocity (rad/s)
- `motors_enabled` - Motor enable/disable (bool, safety gate)

**Fused Sensor Ranges:**
- `fused_front_range` - Fused range for front sector
- `fused_front_left_range` - Fused range for front-left sector
- `fused_front_right_range` - Fused range for front-right sector
- `fused_left_range` - Fused range for left sector
- `fused_right_range` - Fused range for right sector

**Sensor Agreement Scores:**
- `sensor_agreement_front` - Confidence score for front sector (0-1)
- `sensor_agreement_front_left` - Confidence for front-left
- `sensor_agreement_front_right` - Confidence for front-right
- `sensor_agreement_left` - Confidence for left
- `sensor_agreement_right` - Confidence for right

**LiDAR Ranges (raw):**
- `scan_front_ray_range` - Raw LiDAR front range
- `scan_front_left_ray_range` - Raw LiDAR front-left range
- (and similar for other sectors)

**Odometry:**
- `odom_distance` - Total distance traveled (m)
- `odom_direction` - Cardinal direction (N, NE, E, SE, S, SW, W, NW)
- `odom_position_x`, `odom_position_y`, `odom_position_z` - Position
- `odom_orientation_r`, `odom_orientation_p`, `odom_orientation_y` - Orientation

### Obstacle Avoidance Algorithm

The enhanced obstacle avoidance algorithm:

1. **Forward Motion**: Robot moves forward if front sector is clear (> 0.6m threshold)
2. **Obstacle Detection**: When obstacle detected, robot stops immediately
3. **Direction Evaluation**: Checks all 8 directions for clearance
4. **Multi-Criteria Scoring**: 
   - Clearance (distance to obstacle)
   - Sensor agreement (confidence in reading)
   - Direction preference (forward directions preferred)
5. **Best Path Selection**: Chooses direction with highest score
6. **Maneuver Execution**: Turns or reverses toward best direction
7. **Resume**: Returns to forward motion after clearing obstacle

---

## Configuration & Tuning

### Navigation Parameters

Edit `robot_control_client.py` to adjust:

```python
forward_speed = 0.08      # Normal forward speed (m/s)
slow_approach = 0.04      # Slow approach near obstacles (m/s)
turn_speed = 0.15         # Turn speed (rad/s)
threshold = 0.6           # Obstacle reaction distance (m)
danger_threshold = 0.4    # Critical distance (m)
```

### Camera Detection Parameters

Edit `camera_obstacle_detector.py`:

```python
min_contour_area = 500         # Minimum obstacle size (pixels)
max_detection_range = 2.0      # Maximum camera range (m)
min_detection_range = 0.1      # Minimum detection range (m)
distance_calibration_area = 15000.0  # Area-based calibration
```

### Sensor Fusion Parameters

Edit `robot_interface.py`:

```python
lidar_weight = 0.65            # LiDAR weight in fusion
camera_weight = 0.35           # Camera weight in fusion
agreement_threshold = 0.25     # Range difference threshold (m)
sensor_timeout = 2.0           # Camera data timeout (seconds)
_history_window_size = 3       # Temporal filtering window
```

### Camera Settings

Edit `sensor_fusion_hardware.launch.xml`:

```xml
<param name="image_size" value="[800, 600]"/>
<param name="camera_frame_id" value="cowbot_camera"/>
```

### Serial Port Configuration

Edit `sensor_fusion_hardware.launch.xml`:

```xml
<arg name="serial_port" default="/dev/arduino_nano"/>
<arg name="baud_rate" default="57600"/>
```

After changes, rebuild:
```bash
cd ~/cowbot_ws
colcon build --packages-select <package-name>
source install/setup.bash
```

---

## Troubleshooting

### Camera Not Detecting Obstacles

**Symptoms**: Camera topics empty or not publishing

**Solutions**:
```bash
# Check camera device
ls -l /dev/video*

# Check camera is publishing
ros2 topic hz /camera/image_raw

# Verify camera detector is running
ros2 node list | grep camera

# Check for errors in camera detector
ros2 topic echo /camera/obstacle_ranges
```

### LiDAR Not Publishing

**Symptoms**: No `/scan` topic or empty ranges

**Solutions**:
```bash
# Check LiDAR connection
ros2 topic hz /scan

# Check USB devices
ls -l /dev/ttyUSB*

# Verify LiDAR driver is running
ros2 node list | grep lslidar

# Check LiDAR power and connections
```

### Sensor Fusion Not Working

**Symptoms**: No fused parameters or agreement scores all zero

**Solutions**:
```bash
# Verify both sensors are publishing
ros2 topic hz /scan
ros2 topic hz /camera/obstacle_ranges

# Check robot_interface is running
ros2 node list | grep robot_interface

# Check fused parameters exist
ros2 param list | grep fused

# Verify sensor fusion is enabled
ros2 param get /robot_interface fused_front_range
```

### Robot Not Moving

**Symptoms**: Robot doesn't respond to commands

**Solutions**:
```bash
# Check motors are enabled
ros2 param get /robot_interface motors_enabled

# Enable motors if needed
ros2 param set /robot_interface motors_enabled True

# Check cmd_vel is publishing
ros2 topic echo /cowbot/cmd_vel

# Verify motor driver is running
ros2 node list | grep motor
```

### Low Sensor Agreement Scores

**Behavior**: Agreement scores consistently below 0.5

**Explanation**: This is normal and indicates:
- Sensors have different detection capabilities (good for redundancy)
- Camera and LiDAR see different aspects of obstacles
- System uses conservative minimum range for safety

**What to expect**:
- Score > 0.8: Sensors agree well (high confidence)
- Score 0.5-0.8: Moderate agreement (acceptable)
- Score < 0.5: Sensors disagree (system uses conservative approach)

### Package Not Found Errors

**Symptoms**: `package 'cowbot_navigation' not found` or similar

**Solutions**:
```bash
# Build all packages (not just one)
cd ~/cowbot_ws
colcon build --symlink-install

# Source workspace in EVERY terminal
cd ~/cowbot_ws
source install/setup.bash

# Verify packages are available
ros2 pkg list | grep cowbot
```

### Values Are Jumpy (No Temporal Filtering)

**Symptoms**: Fused ranges change abruptly

**Solutions**:
- Wait a few seconds for history buffer to fill (needs 3 frames)
- Check temporal filtering is enabled in code
- Verify sensor data is updating regularly

---

## Project Structure

```
cowbot_ws/
├── src/
│   ├── cowbot_bringup/          # Main launch files
│   │   └── launch/
│   │       ├── bringup.launch.xml
│   │       └── sensor_fusion_hardware.launch.xml
│   ├── cowbot_description/      # Robot URDF/description
│   ├── cowbot_gazebo/           # Gazebo simulation
│   ├── cowbot_navigation/       # Navigation & sensor fusion
│   │   ├── cowbot_navigation/   # Python modules
│   │   ├── launch/              # Launch files
│   │   └── scripts/             # Bash scripts
│   ├── serial_motor/            # Motor driver interface
│   ├── serial_motor_msgs/       # Motor message definitions
│   └── Lslidar_ROS2_driver/     # LiDAR driver
├── build/                        # Build artifacts (gitignored)
├── install/                      # Installed packages (gitignored)
└── log/                          # Build logs (gitignored)
```

---

## Safety Notes

⚠️ **IMPORTANT SAFETY WARNINGS:**

1. **Test in Safe Area**: Always test in an open area away from stairs, drops, or fragile objects
2. **Emergency Stop**: Keep keyboard ready to press Ctrl+C for immediate stop
3. **Motor Enable**: Motors start disabled by default - they enable after system tests pass
4. **Monitor First Run**: Watch the first autonomous run closely
5. **Manual Override**: You can always stop the robot with Ctrl+C
6. **Hardware Check**: Verify all connections before operation

---

## License

MIT License

---

## Contributing

Contributions are welcome! Please ensure:
- Code follows ROS 2 best practices
- All tests pass
- Documentation is updated

---

## Simulation Setup

The Cowbot robot includes a fully functional Gazebo Harmonic simulation with LiDAR, camera, and differential drive capabilities. This is ideal for development and testing without physical hardware.

### What's Included

✅ **Gazebo Harmonic v8** simulation environment
✅ **LiDAR sensor** (LSLidar N10, 270° coverage, ~7 Hz)
✅ **Camera sensor** (800x800 RGB, ~14 Hz, first-person view)
✅ **Differential drive** robot with correct kinematics
✅ **RViz2 visualization** with sensor data display
✅ **Warehouse environment** for testing
✅ **Teleop control** for manual testing

### Prerequisites

- ROS 2 Jazzy installed
- Gazebo Harmonic (gz-harmonic) installed
- RViz2 installed

### Installation

```bash
# Install required packages
sudo apt update
sudo apt install -y \
    ros-jazzy-gz-sim-vendor \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-xacro \
    ros-jazzy-teleop-twist-keyboard

# Build the workspace
cd ~/cowbot/cowbot_ws
colcon build --symlink-install
source install/setup.bash
```

### Launch Simulation

**Complete simulation (Gazebo + RViz):**
```bash
cd ~/cowbot/cowbot_ws
source install/setup.bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

This launches:
- **Gazebo Harmonic** with botbox warehouse world
- **Cowbot robot** with sensors (LiDAR + Camera)
- **RViz2** with pre-configured visualization panels
- **ROS-Gazebo bridges** for sensor data

### Manual Control

In a new terminal, control the robot with keyboard:

```bash
source ~/cowbot/cowbot_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args --remap cmd_vel:=/cowbot/cmd_vel
```

**Controls:**
- `i` = Move forward
- `k` = Stop
- `,` = Move backward  
- `j` = Turn left
- `l` = Turn right
- `u` / `o` = Diagonal movements
- `q` / `z` = Increase/decrease speed

### Monitor Sensors

```bash
# Check LiDAR data rate
ros2 topic hz /cowbot/scan
# Expected: ~7 Hz

# Check camera data rate
ros2 topic hz /camera/image_raw
# Expected: ~14 Hz

# View one LiDAR scan
ros2 topic echo /cowbot/scan --once

# View robot odometry
ros2 topic echo /cowbot/odom

# List all available topics
ros2 topic list
```

### Available Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/cowbot/scan` | sensor_msgs/LaserScan | LiDAR scan data (270°, 0.05-20m) |
| `/camera/image_raw` | sensor_msgs/Image | RGB camera feed (800x800) |
| `/camera/camera_info` | sensor_msgs/CameraInfo | Camera calibration |
| `/cowbot/cmd_vel` | geometry_msgs/Twist | Velocity commands |
| `/cowbot/odom` | nav_msgs/Odometry | Robot odometry |
| `/tf` | tf2_msgs/TFMessage | Transform tree |
| `/tf_static` | tf2_msgs/TFMessage | Static transforms |
| `/joint_states` | sensor_msgs/JointState | Wheel joint states |

### Gazebo Controls

**Camera navigation in Gazebo:**
- **Scroll wheel**: Zoom in/out
- **Middle mouse + drag**: Pan camera
- **Right mouse + drag**: Rotate view
- **Shift + Right mouse + drag**: Move camera position
- **Click robot**: Focus on robot

### RViz Visualization

The simulation automatically configures RViz with:
- **Robot Model**: 3D visualization of the cowbot
- **LiDAR Scan**: Red point cloud showing obstacles
- **Camera**: First-person view from robot camera
- **TF frames**: Coordinate system visualization
- **Odometry**: Robot path/trajectory

### Simulation Architecture

**Gazebo Harmonic Plugins:**
- `gz-sim-diff-drive-system`: Differential drive controller
- `gz-sim-sensors-system`: LiDAR and camera sensors
- `gz-sim-physics-system`: Physics simulation
- `JointStatePublisher`: Publishes wheel joint states
- `PosePublisher`: Publishes robot pose/odometry

**ROS-Gazebo Bridges:**
- Clock sync (`/clock`)
- Camera image and info
- LiDAR scan data
- Velocity commands
- Odometry data

### Robot Specifications (Simulation)

**Differential Drive:**
- Wheel separation: 0.12 m
- Wheel radius: 0.0325 m
- Max velocity: 0.5 m/s
- Two rear wheels + front ball caster

**LiDAR (LSLidar N10):**
- Field of view: 360° (270° effective)
- Range: 0.05 - 20.0 m
- Samples: 270 per scan
- Update rate: ~7 Hz
- Frame: `cowbot/cowbot_base_link/cowbot_lslidar`

**Camera:**
- Resolution: 800x800 pixels
- FOV: 1.396 rad (80°)
- Update rate: ~14 Hz
- Format: RGB8

### Troubleshooting Simulation

**Gazebo won't start:**
```bash
# Check Gazebo installation
gz sim --version

# Should show: Gazebo Sim, version 8.x.x
```

**Robot not visible in Gazebo:**
```bash
# Check if robot spawned
ros2 topic list | grep cowbot

# Check spawn service
ros2 service list | grep spawn
```

**Sensors not publishing:**
```bash
# Verify bridge is running
ros2 node list | grep bridge

# Check bridge topics
ros2 topic list | grep -E "(scan|camera)"
```

**RViz "Message Filter dropping message" warnings:**
- These are **normal** and not critical
- Occur when sensor data arrives faster than RViz can display
- Does not affect simulation functionality

**Performance issues:**
- Close unused applications
- Reduce Gazebo physics update rate (edit world file)
- Reduce camera resolution in plugin config
- Use a dedicated GPU if available

### Network Bridge (Simulation ↔ Hardware)

To connect simulation on one machine with hardware on another:

**On Raspberry Pi (`~/.bashrc`):**
```bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
```

**On Simulation Machine (`~/.bashrc`):**
```bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
```

Both machines will now share ROS 2 topics over the network!

### Development with Simulation

**Test navigation algorithms:**
```bash
# Terminal 1: Launch simulation
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py

# Terminal 2: Run your navigation node
source ~/cowbot/cowbot_ws/install/setup.bash
ros2 run cowbot_navigation robot_control
```

**Record sensor data:**
```bash
# Record a bag file
ros2 bag record /cowbot/scan /camera/image_raw /cowbot/odom

# Play it back later
ros2 bag play <bag_file>
```

**Visualize transforms:**
```bash
# View TF tree
ros2 run rqt_tf_tree rqt_tf_tree

# Echo a specific transform
ros2 run tf2_ros tf2_echo cowbot_base_link cowbot_lslidar
```

---

## Support

For issues or questions:
- Check the Troubleshooting section above
- Review sensor fusion logs for errors
- Verify hardware connections and power
- For simulation issues, see the Simulation Setup section above

---

**Happy Navigating!** 🤖
