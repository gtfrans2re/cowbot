# Simulation Setup Guide - Gazebo + RViz

## Resource Constraints Analysis

Your RPi has:
- 4GB RAM (3.7GB available)
- 64GB SD card (46GB free)

**Gazebo + RViz Requirements:**
- Gazebo: ~2-4GB RAM + GPU acceleration recommended
- RViz: ~500MB-1GB RAM
- **Total: 2.5-5GB RAM** - **NOT feasible on 4GB RPi**

## Recommended Solution: Local Machine + ROS 2 Network Bridge

Run simulation on your local PC/laptop and bridge with RPi over network.

### Advantages:
- ✅ No resource constraints on RPi
- ✅ Better performance with local GPU
- ✅ Can test code changes without impacting hardware workspace
- ✅ Easier development workflow

---

## Setup Options

### Option 1: Local Machine (Recommended)

**Architecture:**
```
Local Machine (Your PC/Laptop)          RPi Server (cowbot)
├── Gazebo (simulation)          ←→     ├── Hardware sensors
├── RViz (visualization)         ←→     ├── Real sensors (optional)
└── ROS 2 Network Bridge         ←→     └── ROS 2 Network Bridge
```

**Requirements:**
- Local machine with ROS 2 Jazzy installed
- Minimum 8GB RAM (16GB recommended)
- GPU support (optional but recommended)
- Network connection to RPi

### Option 2: Docker Container (Alternative)

Run simulation in Docker on a more powerful machine.

### Option 3: Cloud/Remote Machine

Use AWS/GCP/Azure instance for simulation.

---

## Option 1: Local Machine Setup (Step-by-Step)

### Step 1: Install ROS 2 Jazzy on Local Machine

Follow ROS 2 Jazzy installation guide for your OS:
- Ubuntu: https://docs.ros.org/en/jazzy/Installation.html
- Windows/Mac: Use WSL2 or Docker

### Step 2: Clone Workspace to Local Machine

```bash
# On your local machine
cd ~
git clone <your-repo-url> cowbot
cd cowbot/cowbot_ws
```

### Step 3: Install Simulation Dependencies

```bash
sudo apt update
sudo apt install -y \
    gz-jazzy \
    ros-jazzy-rviz2 \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport

# For visualization tools
sudo apt install -y \
    ros-jazzy-rqt \
    ros-jazzy-rqt-common-plugins \
    ros-jazzy-tf2-tools
```

### Step 4: Build Simulation Workspace

```bash
cd ~/cowbot/cowbot_ws
colcon build --symlink-install
source install/setup.bash
```

### Step 5: Set Up ROS 2 Network Bridge

**On RPi (cowbot server):**

```bash
# Find RPi IP address
hostname -I

# Set ROS_DOMAIN_ID (use same on both machines)
export ROS_DOMAIN_ID=0

# Configure ROS 2 to discover other machines
export ROS_LOCALHOST_ONLY=0
```

**On Local Machine:**

```bash
# Set same domain ID
export ROS_DOMAIN_ID=0

# Configure for network discovery
export ROS_LOCALHOST_ONLY=0

# Set RPi IP (replace with actual RPi IP)
export ROS_MASTER_URI=http://<RPI_IP_ADDRESS>:11311
```

Add to `~/.bashrc` on both machines:
```bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
```

### Step 6: Launch Simulation

**On Local Machine:**

```bash
cd ~/cowbot/cowbot_ws
source install/setup.bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

This will launch:
- Gazebo with robot
- RViz with proper visualization
- All necessary nodes

---

## Option 2: Docker Container Setup

### Create Dockerfile for Simulation

Create `~/cowbot/docker/simulation/Dockerfile`:

```dockerfile
FROM osrf/ros:jazzy-desktop-full

# Install dependencies
RUN apt-get update && apt-get install -y \
    ros-jazzy-gazebo-ros-pkgs \
    ros-jazzy-rviz2 \
    ros-jazzy-cv-bridge \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /ros2_ws

# Copy workspace
COPY cowbot_ws /ros2_ws/src/

# Build workspace
RUN colcon build --symlink-install

# Source workspace
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc

CMD ["bash"]
```

### Run Docker Container

```bash
cd ~/cowbot
docker build -t cowbot-simulation -f docker/simulation/Dockerfile .

# Run with GPU support (if available)
docker run -it --rm \
    --network host \
    --env DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    cowbot-simulation

# Or without GPU (software rendering)
docker run -it --rm \
    --network host \
    cowbot-simulation
```

---

## Launch Files to Create

### 1. Complete Simulation Launch (Gazebo + RViz)

### 2. RViz Configuration File

### 3. Network Bridge Setup Script

---

## Next Steps

I'll create:
1. ✅ Complete simulation launch file with Gazebo + RViz
2. ✅ RViz configuration with all your requirements
3. ✅ Network bridging setup guide
4. ✅ Docker alternative setup

Ready to proceed?

