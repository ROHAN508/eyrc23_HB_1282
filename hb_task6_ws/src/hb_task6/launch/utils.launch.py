
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hb_task6',
            executable='startFlag',
        ),
        Node(
            package='hb_task6',
            executable='nextgoal',
        ),
        Node(
            package='hb_task6',
            executable='server',
        ),
        
    ])
