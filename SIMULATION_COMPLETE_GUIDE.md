# Complete Simulation Setup Guide - Gazebo + RViz

## 🎯 Quick Start

**TL;DR**: With only 4GB RAM on your RPi, run simulation on your **local machine** and bridge via ROS 2 network.

---

## 📋 Your Situation

- **RPi**: 4GB RAM, 64GB storage
- **Need**: Gazebo simulation + RViz visualization
- **Problem**: Gazebo needs 2-4GB RAM - won't work on 4GB RPi
- **Solution**: Run simulation on local machine, bridge with RPi

---

## 🏗️ Architecture

```
┌──────────────────────────────────┐      ┌──────────────────────────────────┐
│   Local Machine (Your PC)        │      │   RPi Server (cowbot)            │
│                                  │      │                                  │
│  ✓ Gazebo (Simulation)          │ ←→  │  ✓ Real Hardware                 │
│  ✓ RViz (Visualization)         │      │  ✓ LiDAR, Camera, Motors        │
│  ✓ ROS 2 Network Bridge         │      │  ✓ ROS 2 Network Bridge         │
│                                  │      │                                  │
│  Benefits:                       │      │  Benefits:                       │
│  • More RAM (8GB+)              │      │  • No resource drain             │
│  • GPU acceleration             │      │  • Hardware stays available      │
│  • Better performance           │      │  • Real sensors active           │
└──────────────────────────────────┘      └──────────────────────────────────┘
```

---

## 🚀 Setup Options (Choose One)

### Option 1: Local Machine + Network Bridge ⭐ RECOMMENDED

**Best for**: Most users, easiest setup, best performance

See: [ROS2_NETWORK_BRIDGE.md](./ROS2_NETWORK_BRIDGE.md)

**Steps:**
1. Install ROS 2 Jazzy on local machine
2. Clone workspace to local machine
3. Configure ROS 2 network (ROS_DOMAIN_ID, ROS_LOCALHOST_ONLY)
4. Launch simulation on local, control from RPi

**Time**: ~30 minutes

### Option 2: Docker Container

**Best for**: Isolation, consistency, portability

See: [DOCKER_SIMULATION_SETUP.md](./DOCKER_SIMULATION_SETUP.md)

**Requirements**: 
- Machine with 8GB+ RAM (not RPi!)
- Docker installed

**Time**: ~1 hour (includes Docker setup)

### Option 3: Cloud Instance

**Best for**: When local machine isn't available

**Time**: ~2 hours (includes cloud setup)

---

## 📦 What You'll Get

After setup, you'll have:

### ✅ Gazebo Simulation
- Robot model spawned in world
- Physics simulation
- Sensor plugins (LiDAR, Camera)
- World environment

### ✅ RViz Visualization
- **TF Frames**: All robot coordinate frames
- **Robot Model**: Visual representation
- **Laser Scan**: LiDAR data visualization (size: 0.1)
- **Camera Feed**: Camera image display
- **Reliability**: Best Effort QoS
- **Description Topic**: `/robot_description`

### ✅ Complete Launch File
```bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

This single command launches:
- Gazebo world
- Robot spawn
- RViz with configuration
- Joint state publisher
- All necessary nodes

---

## 🛠️ Installation Steps

### Step 1: Install ROS 2 Jazzy on Local Machine

**Ubuntu:**
```bash
# Follow official guide
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debians.html
```

**Or quick install:**
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
sudo apt update
sudo apt install ros-jazzy-desktop-full
```

### Step 2: Clone Workspace to Local Machine

```bash
cd ~
git clone <your-repo-url> cowbot
cd cowbot/cowbot_ws
```

### Step 3: Install Simulation Dependencies

```bash
sudo apt update
sudo apt install -y \
    ros-jazzy-gazebo-ros-pkgs \
    ros-jazzy-gazebo-ros2-control \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher \
    ros-joint-state-publisher-gui \
    gz-jazzy \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport \
    ros-jazzy-tf2-tools \
    ros-jazzy-rqt \
    ros-jazzy-rqt-common-plugins
```

### Step 4: Build Workspace

```bash
cd ~/cowbot/cowbot_ws
colcon build --symlink-install
source install/setup.bash
```

### Step 5: Configure Network Bridge

**On both machines, edit `~/.bashrc`:**
```bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
```

**Reload:**
```bash
source ~/.bashrc
```

See full guide: [ROS2_NETWORK_BRIDGE.md](./ROS2_NETWORK_BRIDGE.md)

### Step 6: Launch Simulation!

**On Local Machine:**
```bash
cd ~/cowbot/cowbot_ws
source install/setup.bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

**On RPi (separate terminal):**
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 run cowbot_navigation robot_control
```

---

## 🎮 Usage Examples

### Example 1: Visualize Robot in Simulation

```bash
# Terminal 1: Launch simulation
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py

# In RViz, you'll see:
# - Robot model
# - TF frames (base_link, camera, lidar, etc.)
# - Laser scan data
# - Camera feed (optional)
```

### Example 2: Control Simulated Robot

```bash
# Terminal 1: Simulation (on local machine)
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py

# Terminal 2: Control (can run on RPi or local)
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "linear:
  x: 0.2
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.4
"
```

### Example 3: View TF Frames

```bash
# View all frames in terminal
ros2 run tf2_tools view_frames
# Creates: frames.pdf, frames.gv

# View in RViz
# TF display already configured in simulation.rviz

# View using rqt
ros2 run rqt_tf_tree rqt_tf_tree

# Echo specific transform
ros2 run tf2_ros tf2_echo base_link camera_link
```

### Example 4: Compare Simulation vs Hardware

```bash
# Local Machine: Simulation
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py

# RPi: Real hardware
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml

# Monitor from either machine
ros2 topic echo /scan
ros2 topic echo /camera/image_raw
```

---

## 📁 Files Created

### Launch Files
- `cowbot_ws/src/cowbot_gazebo/launch/simulation_with_rviz.launch.py`
  - Complete simulation launch with Gazebo + RViz

### RViz Configuration
- `cowbot_ws/src/cowbot_gazebo/rviz/simulation.rviz`
  - Pre-configured RViz with:
    - TF display (all frames)
    - Robot model
    - Laser scan (size: 0.1, Best Effort QoS)
    - Camera feed
    - Grid

### World Files
- `cowbot_ws/src/cowbot_gazebo/worlds/botbox_warehouse.world`
  - Simple warehouse environment for testing

### Documentation
- `SIMULATION_SETUP.md` - Initial setup guide
- `ROS2_NETWORK_BRIDGE.md` - Network configuration
- `DOCKER_SIMULATION_SETUP.md` - Docker alternative
- `SIMULATION_COMPLETE_GUIDE.md` - This file!

---

## 🔧 Configuration

### RViz Display Settings

Edit `cowbot_ws/src/cowbot_gazebo/rviz/simulation.rviz`:

**Laser Scan:**
- Size: 0.1 (as per your notes)
- Reliability Policy: Best Effort (as per your notes)
- Topic: `/scan`

**Robot Model:**
- Description Topic: `/robot_description` (as per your notes)
- Reliability Policy: Best Effort

**TF Frames:**
- Show all frames including `base_link` (as per your notes)
- Marker Scale: 0.3

### Spawn Position

Edit launch arguments:
```bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py \
    x_spawn:=1.0 \
    y_spawn:=0.5 \
    z_spawn:=0.1 \
    yaw_spawn:=0.0
```

### Headless Mode (No Gazebo GUI)

```bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py headless:=true
```

---

## 🐛 Troubleshooting

### Problem: Gazebo won't start

**Check:**
- Graphics drivers installed
- X11 forwarding (if SSH)
- GPU acceleration available

**Solution:**
```bash
# Test Gazebo separately
gazebo --version

# Try headless mode
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py headless:=true
```

### Problem: RViz doesn't show robot

**Check:**
- Robot spawned in Gazebo
- `/robot_description` topic exists
- Fixed frame set correctly

**Solution:**
```bash
# Check robot description
ros2 topic echo /robot_description

# Check TF frames
ros2 run tf2_tools view_frames

# Verify spawn
ros2 service list | grep spawn
```

### Problem: No laser scan data

**Check:**
- LiDAR plugin loaded in Gazebo
- `/scan` topic exists
- Topic reliability matches RViz config

**Solution:**
```bash
# Check scan topic
ros2 topic hz /scan
ros2 topic echo /scan

# Verify RViz config uses Best Effort QoS
```

### Problem: Network bridge not working

See: [ROS2_NETWORK_BRIDGE.md](./ROS2_NETWORK_BRIDGE.md) - Troubleshooting section

---

## 📚 Additional Resources

### Your Notes Implemented

✅ **TF (base_link)** - Configured in RViz
✅ **Robot Model** - Displayed from `/robot_description`
✅ **Laser Scan** - Size 0.1, Best Effort QoS
✅ **Visualize Frames** - `ros2 run tf2_tools view_frames`
✅ **TF Broadcaster** - Robot state publisher handles this
✅ **Spawn Robot** - Automatic in launch file

### Useful Commands

```bash
# View all TF frames as PDF
ros2 run tf2_tools view_frames

# Monitor TF tree
ros2 run rqt_tf_tree rqt_tf_tree

# Echo transform
ros2 run tf2_ros tf2_echo base_link camera_link

# Monitor all topics
ros2 topic list
ros2 topic hz /scan
ros2 topic hz /camera/image_raw

# Check RViz config
rviz2 -d ~/cowbot_ws/src/cowbot_gazebo/rviz/simulation.rviz
```

---

## ✅ Next Steps

1. **Choose your setup option** (Recommend: Local Machine)
2. **Follow installation steps** above
3. **Configure network bridge** (if using separate machines)
4. **Launch simulation** and test!
5. **Explore RViz** - all features from your notes are configured

---

## 🎉 Summary

You now have:
- ✅ Complete simulation setup with Gazebo + RViz
- ✅ Network bridge capability
- ✅ All features from your notes implemented
- ✅ Documentation for all approaches
- ✅ Troubleshooting guides

**Ready to simulate!** 🚀

For questions or issues, refer to:
- [SIMULATION_SETUP.md](./SIMULATION_SETUP.md) - Initial guide
- [ROS2_NETWORK_BRIDGE.md](./ROS2_NETWORK_BRIDGE.md) - Network setup
- [DOCKER_SIMULATION_SETUP.md](./DOCKER_SIMULATION_SETUP.md) - Docker option

