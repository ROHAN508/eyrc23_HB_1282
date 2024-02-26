
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        Node(
            package='hb_taskbonus',
            executable='startpoint',
        ),
        Node(
            package='hb_taskbonus',
            executable='map1',
        ),
        Node(
            package='hb_taskbonus',
            executable='interp1',
        ),
        Node(
            package='hb_taskbonus',
            executable='interp2',
        ),
        Node(
            package='hb_taskbonus',
            executable='interp3',
        ),
        Node(
            package='hb_taskbonus',
            executable='map2',
        ),
        Node(
            package='hb_taskbonus',
            executable='map3',
        ),
        Node(
            package='hb_taskbonus',
            executable='nextGoalfunc',
        ),
        Node(
            package='hb_taskbonus',
            executable='StopFlag',
        ),
        
    ])
