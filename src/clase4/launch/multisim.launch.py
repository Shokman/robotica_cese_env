# turtlesim/launch/multisim.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import LogInfo

def generate_launch_description():
    launch_dir = os.path.join(get_package_share_directory("clase4"), "launch")
    return LaunchDescription([
        Node(namespace= "turtlesim1", package='turtlesim', executable='turtlesim_node', output='screen'),

        Node(namespace= "turtlesim2", package='turtlesim', executable='turtlesim_node', output='screen'),

        LogInfo(msg=f"Usando mi launchfile del paquete de ROS de la clase 4 el directorio: {launch_dir}"),
    ])
