# Camera-LiDAR Sensor Fusion System

This document describes the camera-LiDAR sensor fusion implementation for enhanced obstacle detection.

## Overview

The system integrates camera-based obstacle detection with LiDAR data to improve obstacle detection accuracy and reliability. The fusion approach uses:

- **LiDAR (LSLidar N10)**: Accurate distance measurements, 270° coverage
- **Camera (800x800 RGB, 80° FOV)**: Visual obstacle detection with edge/contour analysis
- **Sensor Fusion**: Conservative fusion strategy combining both sensors

## Architecture

### 1. Camera Obstacle Detector (`camera_obstacle_detector.py`)
- Subscribes to `/camera/image_raw`
- Uses OpenCV for image processing:
  - Gaussian blur for noise reduction
  - Canny edge detection
  - Morphological operations to connect edges
  - Contour analysis for obstacle detection
- Estimates obstacle distance using:
  - Contour area (larger = closer)
  - Vertical position in frame (lower = closer)
- Divides FOV into 5 sectors matching LiDAR
- Publishes to `/camera/obstacle_ranges`

### 2. Robot Interface with Sensor Fusion (`robot_interface.py`)
- Subscribes to both `/scan` (LiDAR) and `/camera/obstacle_ranges`
- Implements sensor fusion algorithm:
  - **Agreement**: If sensors agree (< 0.2m difference), uses weighted average (60% LiDAR, 40% camera)
  - **Disagreement**: Uses minimum range (conservative approach)
  - **Single sensor**: Falls back to available sensor
- Calculates sensor agreement scores (0-1) for decision quality assessment
- Publishes fused ranges as ROS parameters:
  - `fused_front_range`, `fused_front_left_range`, etc.
  - `sensor_agreement_front`, `sensor_agreement_front_left`, etc.

### 3. Enhanced Robot Control (`robot_control_client.py`)
- Uses fused sensor data for obstacle avoidance
- Multi-criteria decision making:
  - **Clearance**: Distance to obstacle
  - **Agreement**: Sensor confidence (higher = more reliable)
  - **Direction preference**: Forward directions preferred
- Scoring formula: `score = clearance × (0.7 + 0.3 × agreement) × forward_bonus`
- Displays sensor fusion status during operation

## Sectors

Both LiDAR and camera divide the field of view into 5 sectors:

| Sector | Angle | Description |
|--------|-------|-------------|
| Right | -90° | Right side |
| Front-Right | -45° | Front-right diagonal |
| Front | 0° | Straight ahead |
| Front-Left | 45° | Front-left diagonal |
| Left | 90° | Left side |

Back sectors (back, back-left, back-right) use LiDAR only.

## Running the System

### Method 1: Using the launch file
```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 launch cowbot_navigation sensor_fusion.launch.py
```

### Method 2: Running nodes individually
```bash
# Terminal 1: Robot interface
ros2 run cowbot_navigation robot_interface

# Terminal 2: Camera obstacle detector
ros2 run cowbot_navigation camera_obstacle_detector

# Terminal 3: Robot control
ros2 run cowbot_navigation robot_control
```

### With Gazebo simulation
```bash
# Terminal 1: Start Gazebo with cowbot
ros2 launch cowbot_gazebo one_cowbot_warehouse.launch.py

# Terminal 2: Launch sensor fusion system
ros2 launch cowbot_navigation sensor_fusion.launch.py
```

## Monitoring

### Check camera topics
```bash
ros2 topic list | grep camera
ros2 topic echo /camera/image_raw
ros2 topic echo /camera/obstacle_ranges
```

### Check fused sensor parameters
```bash
ros2 param get /robot_interface fused_front_range
ros2 param get /robot_interface sensor_agreement_front
```

### Visualize camera feed (optional)
```bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

## Tuning Parameters

### Camera Obstacle Detector
Edit `camera_obstacle_detector.py`:
- `min_contour_area`: Minimum obstacle size (default: 500 pixels)
- `max_detection_range`: Maximum camera range (default: 2.0m)
- `distance_calibration`: Distance estimation constant (default: 15000.0)

### Sensor Fusion
Edit `robot_interface.py`:
- `lidar_weight`: LiDAR weight in fusion (default: 0.6)
- `camera_weight`: Camera weight in fusion (default: 0.4)
- `agreement_threshold`: Range difference for agreement (default: 0.2m)

### Decision Making
Edit `robot_control_client.py`:
- `threshold`: Obstacle reaction distance (default: 0.6m)
- `forward_speed`: Normal driving speed (default: 0.08 m/s)
- `turn_speed`: Turning speed (default: 0.15 rad/s)

## Benefits

1. **Improved Detection**: Camera detects obstacles LiDAR might miss (dark surfaces, thin objects)
2. **Redundancy**: System continues working if one sensor fails
3. **Confidence Scoring**: Sensor agreement indicates detection reliability
4. **Close-Range**: Camera provides better close-range obstacle detection
5. **Texture-Based**: Camera can detect obstacles based on visual features

## Limitations

1. **Camera Range**: Limited to ~2m (monocular depth estimation)
2. **Lighting**: Camera performance depends on illumination
3. **Computational Cost**: Image processing adds CPU load
4. **Calibration**: Distance estimation requires tuning for specific environments

## Troubleshooting

### Camera not publishing
- Check Gazebo plugin configuration in `cowbot_plugins.gazebo`
- Verify camera topics: `ros2 topic list | grep camera`
- Check if simulation is running properly

### Poor distance estimation
- Adjust `distance_calibration` parameter
- Check lighting conditions in simulation
- Verify obstacles are visible in camera feed

### Sensor disagreement warnings
- Normal when sensors have different detection capabilities
- System uses conservative (minimum) range for safety
- Check sensor agreement scores to assess reliability

## Future Improvements

- Depth camera integration for accurate distance
- Machine learning for obstacle classification
- Adaptive fusion weights based on environment
- Kalman filter for temporal smoothing
- Dynamic calibration based on actual performance
