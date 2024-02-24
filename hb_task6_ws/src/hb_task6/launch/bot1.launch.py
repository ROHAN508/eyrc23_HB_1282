
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hb_task6',
            executable='controllerik',
        ),
        Node(
            package='hb_task6',
            executable='map',
        ),
        Node(
            package='hb_task6',
            executable='interp',
        ),
        
    ])
