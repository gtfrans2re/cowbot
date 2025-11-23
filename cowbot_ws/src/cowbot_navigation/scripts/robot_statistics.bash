#!/usr/bin/bash

# Include the functions library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/robot_functions.bash"

echo "Running Robot Statistics with Bash Script..."
echo "Press Ctrl+C to Terminate..."
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

while :
do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] Robot Telemetry Snapshot"

    odom_dist=$(ros2 param get /robot_interface odom_distance | awk '{print $4}')
    odom_dir=$(ros2 param get /robot_interface odom_direction | awk '{print $4}')

    pos_x=$(ros2 param get /robot_interface odom_position_x | awk '{print $4}')
    pos_y=$(ros2 param get /robot_interface odom_position_y | awk '{print $4}')
    pos_z=$(ros2 param get /robot_interface odom_position_z | awk '{print $4}')

    orient_r=$(ros2 param get /robot_interface odom_orientation_r | awk '{print $4}')
    orient_p=$(ros2 param get /robot_interface odom_orientation_p | awk '{print $4}')
    orient_y=$(ros2 param get /robot_interface odom_orientation_y | awk '{print $4}')

    imu_vel_x=$(ros2 param get /robot_interface imu_angular_velocity_x | awk '{print $4}')
    imu_vel_y=$(ros2 param get /robot_interface imu_angular_velocity_y | awk '{print $4}')
    imu_vel_z=$(ros2 param get /robot_interface imu_angular_velocity_z | awk '{print $4}')

    imu_acc_x=$(ros2 param get /robot_interface imu_linear_acceleration_x | awk '{print $4}')
    imu_acc_y=$(ros2 param get /robot_interface imu_linear_acceleration_y | awk '{print $4}')
    imu_acc_z=$(ros2 param get /robot_interface imu_linear_acceleration_z | awk '{print $4}')

    # Defensive check for missing values
    if [[ -z "$odom_dist" || -z "$pos_x" || -z "$imu_acc_x" ]]; then
        echo "Warning: One or more telemetry values missing. Skipping this snapshot."
        sleep 1
        echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        continue
    fi

    echo "Distance Covered     : $odom_dist m"
    echo "Direction Facing     : $odom_dir"

    echo "Odometry Position    : X=$pos_x  Y=$pos_y  Z=$pos_z"
    echo "Odometry Orientation : Roll=$orient_r  Pitch=$orient_p  Yaw=$orient_y"

    echo "IMU Angular Velocity : X=$imu_vel_x  Y=$imu_vel_y  Z=$imu_vel_z"
    echo "IMU Acceleration     : X=$imu_acc_x  Y=$imu_acc_y  Z=$imu_acc_z"

    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    sleep 1
done
