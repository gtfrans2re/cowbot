from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='cowbot',
        description='Name of the robot (used for topic namespacing)'
    )
    
    linear_speed_arg = DeclareLaunchArgument(
        'linear_speed',
        default_value='0.1',
        description='Maximum linear speed in m/s'
    )
    
    angular_speed_arg = DeclareLaunchArgument(
        'angular_speed',
        default_value='0.3',
        description='Maximum angular speed in rad/s'
    )
    
    robot_name = LaunchConfiguration('robot_name')
    linear_speed = LaunchConfiguration('linear_speed')
    angular_speed = LaunchConfiguration('angular_speed')
    
    # Teleop node with remapping and speed parameters
    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        output='screen',
        remappings=[
            ('cmd_vel', [robot_name, '/cmd_vel'])
        ],
        parameters=[{
            'speed': linear_speed,
            'turn': angular_speed,
        }]
    )
    
    return LaunchDescription([
        robot_name_arg,
        linear_speed_arg,
        angular_speed_arg,
        teleop_node,
    ])
