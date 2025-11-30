# Cowbot Navigation Package

Navigation and obstacle avoidance package for Cowbot robot.

**For complete documentation, see the main [README.md](../../../README.md)**

## Quick Reference

### Main Executables
- `robot_interface` - Sensor fusion bridge node
- `robot_control` - Autonomous navigation with sensor fusion
- `camera_obstacle_detector` - Camera-based obstacle detection

### Usage
```bash
# Launch complete system
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml

# Start navigation
ros2 run cowbot_navigation robot_control
```

See main README.md for full documentation.

