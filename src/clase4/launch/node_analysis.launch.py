import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.actions import LogInfo
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import TextSubstitution


def generate_launch_description():

    # Declare the launch arguments
    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='false',
        choices=['true', 'false'],
        description='Flag to enable rqt gui')
    gui = LaunchConfiguration('gui')

    mi_perspectiva = os.path.join(
        get_package_share_directory('clase4'),
        'config', "view_nodes.perspective")
    
    mi_mensaje = LogInfo(msg=[
        'Abriendo RQT con la perspectiva: ', mi_perspectiva])
    
    launch_nodos = IncludeLaunchDescription(
        os.path.join(get_package_share_directory('clase4'),'launch', 'multisim.launch.py')
    )

    rqt_gui_node = Node(
        package='rqt_gui',
        executable='rqt_gui',
        name='mi_rqt_gui',
        arguments=['--perspective-file', TextSubstitution(text=mi_perspectiva)],
        condition=IfCondition(gui))

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(gui_arg)

    # Add any actions
    ld.add_action(launch_nodos)
    ld.add_action(rqt_gui_node)
    ld.add_action(mi_mensaje)

    return ld
