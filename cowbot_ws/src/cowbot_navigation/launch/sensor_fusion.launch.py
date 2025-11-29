#!/usr/bin/env python3
"""Launch file for camera-LiDAR sensor fusion system."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Launch robot interface, camera detector, and fusion-based control."""
    
    return LaunchDescription([
        # Robot interface with sensor fusion
        Node(
            package='cowbot_navigation',
            executable='robot_interface',
            name='robot_interface',
            output='screen',
            parameters=[
                {'motors_enabled': False}
            ]
        ),
        
        # Camera obstacle detector
        Node(
            package='cowbot_navigation',
            executable='camera_obstacle_detector',
            name='camera_obstacle_detector',
            output='screen'
        ),
        
        # Robot control with sensor fusion
        Node(
            package='cowbot_navigation',
            executable='robot_control',
            name='robot_control',
            output='screen'
        ),
    ])
