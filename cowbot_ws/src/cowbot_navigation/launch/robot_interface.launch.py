#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cowbot_navigation',
            executable='robot_interface',
            name='robot_interface',
            output='screen',
            parameters=[],
        ),
    ])
