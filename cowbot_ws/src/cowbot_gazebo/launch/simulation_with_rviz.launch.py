#!/usr/bin/env python3
"""
Complete simulation launch file with Gazebo and RViz.
Launches Gazebo world, spawns robot, and opens RViz with proper configuration.
"""

import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
    ExecuteProcess,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get package directories
    gazebo_pkg = get_package_share_directory("cowbot_gazebo")
    description_pkg = get_package_share_directory("cowbot_description")

    # Launch arguments
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    headless = LaunchConfiguration("headless")
    world_name = LaunchConfiguration("world_name")
    robot_name = LaunchConfiguration("robot_name")
    x_spawn = LaunchConfiguration("x_spawn")
    y_spawn = LaunchConfiguration("y_spawn")
    z_spawn = LaunchConfiguration("z_spawn")
    yaw_spawn = LaunchConfiguration("yaw_spawn")

    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock if true",
    )
    declare_use_rviz = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz if true",
    )
    declare_headless = DeclareLaunchArgument(
        "headless",
        default_value="false",
        description="Run Gazebo in headless mode (no GUI) if true",
    )
    declare_world_name = DeclareLaunchArgument(
        "world_name",
        default_value="botbox_warehouse",
        description="Gazebo world name",
    )
    declare_robot_name = DeclareLaunchArgument(
        "robot_name",
        default_value="cowbot",
        description="Robot name",
    )
    declare_x_spawn = DeclareLaunchArgument(
        "x_spawn", default_value="0.5", description="X spawn position"
    )
    declare_y_spawn = DeclareLaunchArgument(
        "y_spawn", default_value="-0.75", description="Y spawn position"
    )
    declare_z_spawn = DeclareLaunchArgument(
        "z_spawn", default_value="0.1", description="Z spawn position"
    )
    declare_yaw_spawn = DeclareLaunchArgument(
        "yaw_spawn", default_value="1.52", description="Yaw spawn orientation"
    )

    # RViz configuration file path
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("cowbot_gazebo"), "rviz", "simulation.rviz"]
    )

    # Launch Gazebo world
    gazebo_world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_pkg, "launch", "botbox_world.launch.xml")
        ),
        launch_arguments={
            "map_name": world_name,
            "headless": headless,
        }.items(),
    )

    # Spawn robot in Gazebo (delayed)
    spawn_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_pkg, "launch", "spawn_cowbot.launch.xml")
        ),
        launch_arguments={
            "robot_name": robot_name,
            "x_spawn": x_spawn,
            "y_spawn": y_spawn,
            "z_spawn": z_spawn,
            "yaw_spawn": yaw_spawn,
        }.items(),
    )

    # Delay spawn after world loads
    delayed_spawn = TimerAction(period=3.0, actions=[spawn_robot_launch])

    # RViz node
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        condition=IfCondition(use_rviz),
        parameters=[{"use_sim_time": use_sim_time}],
    )

    # Joint State Publisher (for manual joint control if needed)
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )

    # TF2 tools - view frames command (optional)
    # Users can run: ros2 run tf2_tools view_frames

    return LaunchDescription(
        [
            # Launch arguments
            declare_use_sim_time,
            declare_use_rviz,
            declare_headless,
            declare_world_name,
            declare_robot_name,
            declare_x_spawn,
            declare_y_spawn,
            declare_z_spawn,
            declare_yaw_spawn,
            # Launch Gazebo world
            gazebo_world_launch,
            # Spawn robot (delayed)
            delayed_spawn,
            # Launch RViz
            rviz_node,
            # Joint State Publisher GUI
            joint_state_publisher_gui,
        ]
    )


