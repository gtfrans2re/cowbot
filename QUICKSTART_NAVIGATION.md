# Cowbot Navigation - Quick Start Guide

## Installation Complete! ✅

Your LiDAR obstacle detection and avoidance system is now installed.

## Quick Start

### Step 1: Start Your Robot Hardware

First, launch your robot's hardware interface (motors, LiDAR, etc.):

```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 launch cowbot_bringup bringup.launch.xml
```

### Step 2: Start the Robot Interface (New Terminal)

Open a new terminal and start the robot_interface node:

```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 launch cowbot_navigation robot_interface.launch.py
```

This node bridges your LiDAR data with velocity commands.

### Step 3: Choose Your Control Method (New Terminal)

Open another terminal and run one of these:

#### Option A: Python with Obstacle Avoidance (Recommended)

```bash
cd ~/cowbot_ws
source install/setup.bash
ros2 run cowbot_navigation robot_control_classed
```

This will:
- Run movement tests
- Start autonomous obstacle avoidance
- Drive forward and avoid obstacles automatically

#### Option B: Bash Script Patrol

```bash
cd ~/cowbot_ws
source install/setup.bash
cd src/cowbot_navigation/scripts
./robot_functions.bash
```

#### Option C: Monitor Robot Statistics

```bash
cd ~/cowbot_ws
source install/setup.bash
cd src/cowbot_navigation/scripts
./robot_statistics.bash
```

## What Each Terminal Shows

**Terminal 1** (Hardware):
- Motor driver status
- LiDAR data
- Odometry updates
- IMU readings

**Terminal 2** (robot_interface):
- Parameter updates
- Scan processing
- cmd_vel publishing

**Terminal 3** (Control):
- Movement commands
- Obstacle detection
- Direction decisions

## Testing Without Hardware (Simulation)

If you want to test in simulation first, you would typically:

1. Launch Gazebo simulation instead of hardware
2. Continue with steps 2 and 3 as above

## Stopping the Robot

Press `Ctrl+C` in the control terminal (Terminal 3) to stop autonomous movement.
The robot will stop immediately.

## Adjusting Behavior

Edit these values in the control scripts to tune performance:

**In robot_control_classed.py or robot_control_noclass.py:**

```python
forward_speed = 0.2   # Speed when moving forward (m/s)
turn_speed = 0.5      # Speed when turning (rad/s)
threshold = 0.4       # Minimum safe distance (m)
```

**In robot_functions.bash:**

```bash
threshold=0.300       # Minimum safe distance (m)
```

## Troubleshooting

### Robot doesn't move
- Check that robot_interface is running (Terminal 2)
- Verify /cmd_vel topic: `ros2 topic echo /cmd_vel`
- Check parameters: `ros2 param list | grep robot_interface`

### No obstacle detection
- Verify LiDAR is publishing: `ros2 topic echo /scan`
- Check scan parameters: `ros2 param get /robot_interface scan_front_ray_range`

### Robot turns randomly
- LiDAR may be seeing obstacles
- Increase threshold value
- Check LiDAR is mounted correctly

## Files Created

```
~/cowbot_ws/src/cowbot_navigation/
├── cowbot_navigation/
│   ├── robot_interface.py          # Main bridge node
│   ├── robot_control_classed.py    # OOP control with avoidance
│   └── robot_control_noclass.py    # Procedural control
├── scripts/
│   ├── robot_functions.bash        # Bash patrol
│   └── robot_statistics.bash       # Telemetry display
├── launch/
│   └── robot_interface.launch.py   # Launch file
└── README.md                        # Full documentation
```

## Next Steps

1. Test with obstacles in front of the robot
2. Tune speed and threshold values for your environment
3. Modify avoidance algorithm in the Python scripts
4. Integrate robot_interface into your main launch file

## Full Documentation

See `~/cowbot_ws/src/cowbot_navigation/README.md` for complete documentation.

---

Happy navigating! 🤖
