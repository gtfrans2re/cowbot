# Hardware Sensor Fusion Setup Guide

This guide will help you run the camera-LiDAR sensor fusion system on your physical cowbot robot.

## Prerequisites Checklist

Before starting, ensure:
- [ ] Cowbot hardware is powered on
- [ ] Arduino/motor controller connected to `/dev/arduino_nano` (or adjust serial port)
- [ ] LSLidar N10 is connected and powered
- [ ] Camera is connected (Raspberry Pi camera or USB camera at `/dev/video0`)
- [ ] All cables are securely connected
- [ ] Robot is in a safe testing area

## Quick Start

### Step 1: Source Your Workspace
```bash
cd ~/cowbot_ws
source install/setup.bash
```

### Step 2: Launch Hardware with Sensor Fusion
```bash
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml
```

This will start:
- ✅ Motor driver (serial_motor)
- ✅ LiDAR driver (lslidar_driver)
- ✅ Camera driver (v4l2_camera)
- ✅ Camera obstacle detector
- ✅ Robot interface with sensor fusion

### Step 3: Verify All Systems Are Running

Open a new terminal and check:

```bash
# Check all topics
ros2 topic list

# You should see these topics:
# /scan                      (LiDAR)
# /camera/image_raw          (Camera feed)
# /camera/obstacle_ranges    (Camera detections)
# /cowbot/cmd_vel            (Motor commands)
# /odom                      (Odometry)
```

### Step 4: Monitor Sensor Fusion

```bash
# Check fused sensor data
ros2 param get /robot_interface fused_front_range
ros2 param get /robot_interface sensor_agreement_front

# Watch sensor data in real-time
watch -n 0.5 "ros2 param get /robot_interface fused_front_range && ros2 param get /robot_interface sensor_agreement_front"

# Check camera obstacle ranges
ros2 topic echo /camera/obstacle_ranges
```

### Step 5: Visualize Camera Feed (Optional)

```bash
# In a new terminal
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

### Step 6: Start Autonomous Navigation

Once everything is verified, in a new terminal:

```bash
ros2 run cowbot_navigation robot_control
```

The robot will:
1. Run system tests (move forward, turn, etc.)
2. Enable motors
3. Start autonomous navigation with sensor fusion

## Alternative: Manual Control First

If you want to test manually before autonomous mode:

```bash
# Terminal 1: Launch hardware
ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml

# Terminal 2: Keyboard teleop
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cowbot/cmd_vel
```

Then monitor the sensor fusion while driving manually:
```bash
# Terminal 3: Monitor fusion
watch -n 0.5 "echo '=== Fused Ranges ===' && \
ros2 param get /robot_interface fused_front_range && \
ros2 param get /robot_interface fused_left_range && \
ros2 param get /robot_interface fused_right_range && \
echo '=== Agreement Scores ===' && \
ros2 param get /robot_interface sensor_agreement_front && \
ros2 param get /robot_interface sensor_agreement_left && \
ros2 param get /robot_interface sensor_agreement_right"
```

## Troubleshooting

### Camera not found
```bash
# Check available cameras
ls -l /dev/video*

# If camera is on different device, edit launch file
# and change image_size if needed
```

### LiDAR not publishing
```bash
# Check LiDAR connection
ros2 topic hz /scan

# If no data, check LiDAR power and USB connection
```

### Motor driver issues
```bash
# Check serial port
ls -l /dev/arduino_nano
ls -l /dev/ttyUSB* /dev/ttyACM*

# Adjust serial_port argument if needed
```

### Low sensor agreement scores
This is normal! It means:
- **Score > 0.8**: Sensors agree well (good)
- **Score 0.5-0.8**: Moderate agreement (okay)
- **Score < 0.5**: Sensors disagree (system uses conservative minimum)

Disagreement can happen when:
- Camera detects obstacle LiDAR misses (good!)
- Different sensor ranges or blind spots
- Lighting conditions affect camera

## Safety Tips

🛑 **IMPORTANT SAFETY NOTES:**

1. **Start in Safe Area**: Test in open area away from stairs, drops, or fragile objects
2. **Emergency Stop**: Keep keyboard ready to press Ctrl+C to stop
3. **Motor Enable**: Motors start disabled; they enable after tests pass
4. **Manual Override**: You can always stop with Ctrl+C
5. **Monitor First Run**: Watch the first autonomous run closely

## Customizing Parameters

### Adjust Camera Settings
Edit `/home/cowbot/cowbot_ws/src/cowbot_bringup/launch/sensor_fusion_hardware.launch.xml`:

```xml
<!-- Change resolution -->
<param name="image_size" value="[640, 480]"/>

<!-- Change encoding if needed -->
<param name="output_encoding" value="rgb8"/>
```

### Tune Obstacle Detection
Edit `/home/cowbot/cowbot_ws/src/cowbot_navigation/cowbot_navigation/camera_obstacle_detector.py`:

```python
self.min_contour_area = 500         # Smaller = more sensitive
self.max_detection_range = 2.0      # Maximum camera range
self.distance_calibration = 15000.0 # Adjust for distance accuracy
```

### Adjust Navigation Behavior
Edit `/home/cowbot/cowbot_ws/src/cowbot_navigation/cowbot_navigation/robot_control_client.py`:

```python
forward_speed = 0.08      # Increase/decrease speed
turn_speed = 0.15         # Adjust turn rate
threshold = 0.6           # Distance to react to obstacles
```

After changes, rebuild:
```bash
cd ~/cowbot_ws
colcon build --packages-select cowbot_navigation cowbot_bringup
source install/setup.bash
```

## Monitoring Commands Summary

```bash
# Check all topics
ros2 topic list

# Check topic rates
ros2 topic hz /scan
ros2 topic hz /camera/image_raw
ros2 topic hz /camera/obstacle_ranges

# Monitor specific topics
ros2 topic echo /camera/obstacle_ranges
ros2 topic echo /scan --no-arr

# Check parameters
ros2 param list | grep fused
ros2 param list | grep agreement

# Get specific parameters
ros2 param get /robot_interface fused_front_range
ros2 param get /robot_interface sensor_agreement_front
```

## What to Expect

When running correctly, you should see:
- LiDAR publishing at ~10 Hz
- Camera publishing at ~30 Hz
- Camera obstacle ranges updating
- Fused ranges combining both sensors
- Agreement scores showing sensor confidence
- Robot navigating while avoiding obstacles

The system will prefer forward movement when clear, and intelligently choose the best direction when obstacles are detected using both sensor inputs.

## Next Steps

Once everything works:
1. Test in different lighting conditions
2. Try obstacles of different materials (wood, metal, fabric)
3. Compare detection with LiDAR-only vs. sensor fusion
4. Tune parameters for your specific environment
5. Add autonomous mission waypoints (future enhancement)

---

**You're ready to test!** Start with the Quick Start section above.
