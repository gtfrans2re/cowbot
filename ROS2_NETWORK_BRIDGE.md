# ROS 2 Network Bridge Setup Guide

## Overview

This guide explains how to set up ROS 2 network communication between your **local machine** (running Gazebo simulation) and your **RPi server** (running hardware).

## Why Network Bridge?

- **Resource Constraints**: RPi has only 4GB RAM - insufficient for Gazebo
- **Better Performance**: Local machine has more power and GPU support
- **Development Flexibility**: Test simulation without impacting hardware workspace
- **Parallel Operation**: Run both simulation and hardware simultaneously

## Architecture

```
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│   Local Machine (Your PC)       │         │   RPi Server (cowbot)           │
│                                 │         │                                 │
│  ┌──────────────────────────┐  │         │  ┌──────────────────────────┐  │
│  │  Gazebo (Simulation)     │  │         │  │  Hardware Sensors        │  │
│  │  - Robot simulation      │  │         │  │  - LiDAR                 │  │
│  │  - Physics engine        │  │         │  │  - Camera                │  │
│  └──────────────────────────┘  │         │  └──────────────────────────┘  │
│                                 │         │                                 │
│  ┌──────────────────────────┐  │         │  ┌──────────────────────────┐  │
│  │  RViz (Visualization)    │  │  ←───→  │  │  Robot Control Nodes     │  │
│  │  - TF visualization      │  │         │  │  - robot_interface       │  │
│  │  - Sensor data display   │  │         │  │  - robot_control         │  │
│  └──────────────────────────┘  │         │  └──────────────────────────┘  │
│                                 │         │                                 │
│  ROS 2 Domain ID: 0             │         │  ROS 2 Domain ID: 0             │
│  ROS_LOCALHOST_ONLY=0           │         │  ROS_LOCALHOST_ONLY=0           │
└─────────────────────────────────┘         └─────────────────────────────────┘
                 │                                      │
                 └────────── Network Connection ────────┘
```

## Prerequisites

1. **Both machines on same network** (WiFi or Ethernet)
2. **ROS 2 Jazzy installed** on both machines
3. **Firewall configured** to allow ROS 2 communication (ports 7400-7500, 11311)
4. **Network connectivity** between machines

## Step-by-Step Setup

### Step 1: Find IP Addresses

**On RPi (cowbot server):**
```bash
hostname -I
# Example output: 192.168.1.100
```

**On Local Machine:**
```bash
hostname -I
# Example output: 192.168.1.50
```

**Note down both IP addresses!**

### Step 2: Configure ROS 2 on RPi

**On RPi (cowbot server), edit `~/.bashrc`:**
```bash
nano ~/.bashrc
```

Add these lines at the end:
```bash
# ROS 2 Network Configuration
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0

# Optional: Set ROS_DISCOVERY_SERVER for better discovery
# export ROS_DISCOVERY_SERVER=192.168.1.50:11811
```

Save and reload:
```bash
source ~/.bashrc
```

### Step 3: Configure ROS 2 on Local Machine

**On Local Machine, edit `~/.bashrc`:**
```bash
nano ~/.bashrc
```

Add these lines at the end:
```bash
# ROS 2 Network Configuration
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0

# Optional: Discovery server (if using)
# export ROS_DISCOVERY_SERVER=192.168.1.50:11811
```

Save and reload:
```bash
source ~/.bashrc
```

### Step 4: Configure Firewall (if needed)

**On RPi:**
```bash
# Allow ROS 2 ports (if using ufw)
sudo ufw allow 7400:7500/udp
sudo ufw allow 11311/tcp
```

**On Local Machine:**
```bash
# Allow ROS 2 ports (if using ufw)
sudo ufw allow 7400:7500/udp
sudo ufw allow 11311/tcp
```

### Step 5: Test Network Connection

**On RPi, test ping to local machine:**
```bash
ping <LOCAL_MACHINE_IP>
# Example: ping 192.168.1.50
```

**On Local Machine, test ping to RPi:**
```bash
ping <RPI_IP>
# Example: ping 192.168.1.100
```

### Step 6: Test ROS 2 Discovery

**On RPi, start a simple node:**
```bash
ros2 run demo_nodes_cpp talker
```

**On Local Machine, listen for topics:**
```bash
ros2 topic echo /chatter
```

If you see messages, **network bridge is working!** 🎉

## Usage Scenarios

### Scenario 1: Run Simulation on Local, Control from RPi

**On Local Machine:**
```bash
cd ~/cowbot/cowbot_ws
source install/setup.bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

**On RPi:**
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 run cowbot_navigation robot_control
```

**Result:** Robot in simulation is controlled by code running on RPi!

### Scenario 2: View Hardware Data from Local Machine

**On RPi:**
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml
```

**On Local Machine:**
```bash
cd ~/cowbot/cowbot_ws
source install/setup.bash
rviz2
# In RViz, subscribe to /scan, /camera/image_raw, etc.
```

### Scenario 3: Compare Simulation vs Hardware

Run both simultaneously:
- Local: Simulation
- RPi: Hardware

Monitor topics from either machine!

## Troubleshooting

### Problem: Nodes not discovering each other

**Solution:**
```bash
# Check ROS_DOMAIN_ID matches on both machines
echo $ROS_DOMAIN_ID

# Check ROS_LOCALHOST_ONLY is 0
echo $ROS_LOCALHOST_ONLY

# Verify network connectivity
ping <other_machine_ip>
```

### Problem: Firewall blocking communication

**Solution:**
```bash
# Temporarily disable firewall for testing
sudo ufw disable

# Or configure proper rules (see Step 4)
```

### Problem: Topics not visible

**Solution:**
```bash
# List all topics (should see topics from both machines)
ros2 topic list

# Check specific topic
ros2 topic hz /scan

# Verify topic is publishing from remote machine
ros2 topic info /scan
```

### Problem: High latency/delays

**Solutions:**
1. Use wired connection instead of WiFi
2. Ensure both machines on same network segment
3. Check network bandwidth usage
4. Use ROS_DISCOVERY_SERVER for better performance (optional)

## Advanced: Discovery Server (Optional)

For better performance and control, use ROS 2 Discovery Server:

**On Local Machine:**
```bash
ros2 run ros2discovery fastdds discovery --server-id 0
```

**On both machines, set:**
```bash
export ROS_DISCOVERY_SERVER=192.168.1.50:11811
```

## Security Considerations

1. **Private Network**: Only use on trusted private networks
2. **Firewall**: Configure proper firewall rules
3. **Domain ID**: Use unique domain IDs for different projects
4. **Credentials**: ROS 2 doesn't use authentication - secure your network

## Summary

✅ **Network bridge enables:**
- Running simulation on powerful local machine
- Keeping RPi resources free for hardware
- Testing code changes without impacting hardware workspace
- Comparing simulation vs hardware behavior
- Remote monitoring and debugging

🚀 **Ready to bridge!**

