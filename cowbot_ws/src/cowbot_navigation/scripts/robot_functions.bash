#!/usr/bin/bash

# Robot functions library for cowbot

# ========================
# Getter functions for scan ranges
# ========================

get_scan_right_ray_range() {
    ros2 param get /robot_interface scan_right_ray_range | awk '{print $4}'
}

get_scan_front_right_ray_range() {
    ros2 param get /robot_interface scan_front_right_ray_range | awk '{print $4}'
}

get_scan_front_ray_range() {
    ros2 param get /robot_interface scan_front_ray_range | awk '{print $4}'
}

get_scan_front_left_ray_range() {
    ros2 param get /robot_interface scan_front_left_ray_range | awk '{print $4}'
}

get_scan_left_ray_range() {
    ros2 param get /robot_interface scan_left_ray_range | awk '{print $4}'
}

# ========================
# Setter functions for cmd_vel
# ========================

set_cmd_vel_linear() {
    ros2 param set /robot_interface cmd_vel_linear "$1"
    return 0
}

set_cmd_vel_angular() {
    ros2 param set /robot_interface cmd_vel_angular "$1"
    return 0
}

# ========================
# Simple robot patrol implementation
# ========================

run_simple_patrol() {
    echo "Running Simple Robot Patrol with Bash Script..."
    echo "Press Ctrl+C to Terminate..."

    # Make sure that the robot is stopped initially
    set_cmd_vel_linear 0.000
    set_cmd_vel_angular 0.000

    # Set obstacle distance threshold
    threshold=0.300

    # Main while loop for simple robot patrol
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    while :
    do
        # Get the left, front, right scan range values
        ff_range=$(get_scan_front_ray_range)
        echo "front range: $ff_range meters"
        
        # Check if front range is under threshold
        front_free=$(echo "$ff_range > $threshold" | bc -l)
        echo "front_free: $front_free"
        
        # If front range is less than threshold
        if [[ "$front_free" == "0" ]]; then
            # Check which direction to turn
            ll_range=$(get_scan_left_ray_range)
            echo "left range: $ll_range meters"
            rr_range=$(get_scan_right_ray_range)
            echo "right range: $rr_range meters"
            
            if (( $(echo "$ll_range > $rr_range" | bc -l ) )); then
                # Turn left for roughly 90 degrees
                echo "turning left..."
                set_cmd_vel_angular 0.31416
            else
                # Turn right for roughly 90 degrees
                echo "turning right..."
                set_cmd_vel_angular -0.31416
            fi
            
            # Wait for the robot to turn - tune delay accordingly
            sleep 1.500
            # Set angular velocity back to zero
            set_cmd_vel_angular 0.000
        else
            # If front range is more than threshold
            # Move forward for roughly (front range - threshold) meters
            dist_to_move=$(echo "$ff_range - $threshold" | bc -l)
            # Calculate time with fixed speed of 0.1 m/s
            time_to_move=$(echo "$dist_to_move / 0.100" | bc -l)
            # Subtract 1 second for parameter setting delay
            time_to_move=$(echo "$time_to_move - 1.000" | bc -l)
            echo "dist_to_move: $dist_to_move meters"
            echo "time_to_move: $time_to_move seconds"
            echo "moving forward..."
            set_cmd_vel_linear 0.100
            sleep $time_to_move
            # Set linear velocity back to zero
            set_cmd_vel_linear 0.000
        fi
        
        # Print a divider line to show iteration is complete
        echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    done
}

# If script is run directly (not sourced), execute the patrol
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_simple_patrol
fi

# End of Code
