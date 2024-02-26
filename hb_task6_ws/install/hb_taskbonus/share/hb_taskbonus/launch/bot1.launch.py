
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hb_taskbonus',
            executable='controller1',
        ),
        Node(
            package='hb_taskbonus',
            executable='map1',
        ),
        Node(
            package='hb_taskbonus',
            executable='interp1',
        ),
        
    ])
