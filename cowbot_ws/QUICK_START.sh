#!/bin/bash
# Quick Start Script for Hardware Sensor Fusion

echo "=========================================="
echo "  Cowbot Sensor Fusion - Quick Start"
echo "=========================================="
echo ""
echo "This script provides commands for testing sensor fusion on hardware."
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== STEP 1: Source Workspace ===${NC}"
echo "cd ~/cowbot_ws && source install/setup.bash"
echo ""

echo -e "${BLUE}=== STEP 2: Launch Hardware with Sensor Fusion ===${NC}"
echo "ros2 launch cowbot_bringup sensor_fusion_hardware.launch.xml"
echo ""

echo -e "${YELLOW}In a new terminal:${NC}"
echo ""

echo -e "${BLUE}=== STEP 3: Verify Topics ===${NC}"
echo "ros2 topic list"
echo "ros2 topic hz /scan"
echo "ros2 topic hz /camera/image_raw"
echo ""

echo -e "${BLUE}=== STEP 4: Monitor Sensor Fusion ===${NC}"
echo "# Check fused ranges:"
echo "ros2 param get /robot_interface fused_front_range"
echo "ros2 param get /robot_interface sensor_agreement_front"
echo ""
echo "# Watch in real-time:"
echo "watch -n 0.5 'ros2 param get /robot_interface fused_front_range'"
echo ""

echo -e "${BLUE}=== STEP 5: View Camera Feed (Optional) ===${NC}"
echo "ros2 run rqt_image_view rqt_image_view /camera/image_raw"
echo ""

echo -e "${BLUE}=== STEP 6: Start Autonomous Navigation ===${NC}"
echo "ros2 run cowbot_navigation robot_control"
echo ""

echo -e "${GREEN}=== ALTERNATIVE: Manual Control First ===${NC}"
echo "# Terminal 1: Launch hardware (from Step 2)"
echo "# Terminal 2: Teleop"
echo "ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cowbot/cmd_vel"
echo ""

echo -e "${YELLOW}=== Emergency Stop ===${NC}"
echo "Press Ctrl+C in any terminal to stop"
echo ""

echo "=========================================="
echo "See HARDWARE_SETUP_GUIDE.md for details"
echo "=========================================="
