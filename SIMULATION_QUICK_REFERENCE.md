# Simulation Quick Reference Card

## 🚀 Launch Simulation

```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

## 📋 All Your Notes Implemented

✅ **TF (base_link)** - Displayed in RViz
✅ **Robot Model** - From `/robot_description` topic
✅ **Laser Scan** - Size: 0.1, Reliability: Best Effort
✅ **Visualize Frames** - `ros2 run tf2_tools view_frames`
✅ **TF Broadcaster** - Robot state publisher
✅ **Spawn Robot** - Automatic in launch

## 🔧 Useful Commands

### View TF Frames
```bash
# As PDF
ros2 run tf2_tools view_frames

# In RViz (already configured)
# Just launch simulation - TF display is enabled

# Tree view
ros2 run rqt_tf_tree rqt_tf_tree
```

### Control Robot
```bash
# Move forward
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "linear: {x: 0.2}" "angular: {z: 0.0}"

# Turn
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "linear: {x: 0.0}" "angular: {z: 0.4}"
```

### Monitor Topics
```bash
# List all topics
ros2 topic list

# Check scan data
ros2 topic hz /scan
ros2 topic echo /scan

# Check camera
ros2 topic hz /camera/image_raw
```

## 🌐 Network Bridge Setup

**On both machines:**
```bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
```

Add to `~/.bashrc` for permanent setup.

## 📚 Full Guides

- **SIMULATION_COMPLETE_GUIDE.md** - Complete setup guide
- **ROS2_NETWORK_BRIDGE.md** - Network configuration details
- **DOCKER_SIMULATION_SETUP.md** - Docker alternative

## ⚡ Quick Troubleshooting

**Gazebo won't start?**
- Check GPU drivers
- Try headless mode: `headless:=true`

**RViz shows no robot?**
- Check `/robot_description` topic exists
- Verify robot spawned in Gazebo
- Check fixed frame is set correctly

**Network bridge not working?**
- Verify ROS_DOMAIN_ID matches on both machines
- Check ROS_LOCALHOST_ONLY=0
- Test ping between machines

