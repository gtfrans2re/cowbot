#!/usr/bin/bash

echo "==================================="
echo "Cowbot Navigation System Test"
echo "==================================="

# Source ROS2 workspace
source /home/cowbot/cowbot_ws/install/setup.bash

echo ""
echo "Checking if package is built..."
if ros2 pkg list | grep -q "cowbot_navigation"; then
    echo "[OK] cowbot_navigation package found"
else
    echo "[FAIL] cowbot_navigation package NOT found"
    echo "Run: cd ~/cowbot_ws && colcon build --packages-select cowbot_navigation"
    exit 1
fi

echo ""
echo "Checking executables..."
for exec in robot_interface robot_control_classed robot_control_noclass; do
    if ros2 pkg executables cowbot_navigation | grep -q "$exec"; then
        echo "[OK] $exec available"
    else
        echo "[FAIL] $exec NOT available"
    fi
done

echo ""
echo "Checking launch files..."
if [ -f "/home/cowbot/cowbot_ws/install/cowbot_navigation/share/cowbot_navigation/launch/robot_interface.launch.py" ]; then
    echo "[OK] robot_interface.launch.py installed"
else
    echo "[FAIL] robot_interface.launch.py NOT installed"
fi

echo ""
echo "Checking bash scripts..."
for script in robot_functions.bash robot_statistics.bash; do
    if [ -f "/home/cowbot/cowbot_ws/install/cowbot_navigation/share/cowbot_navigation/scripts/$script" ]; then
        echo "[OK] $script installed"
    else
        echo "[FAIL] $script NOT installed"
    fi
done

echo ""
echo "==================================="
echo "Test Complete!"
echo "==================================="
echo ""
echo "To use the navigation system:"
echo "1. Start your robot hardware (bringup.launch.xml)"
echo "2. Start robot_interface: ros2 launch cowbot_navigation robot_interface.launch.py"
echo "3. Run one of the control methods (see README.md)"
echo ""
