#!/usr/bin/env python3
"""
Launch RViz visualization for the mycobot robot.

This launch file sets up the complete visualization environment for the mycobot robot,
including robot state publisher, joint state publisher, and RViz2. It handles loading
and processing of URDF/XACRO files and controller configurations.

:author: Addison Sears-Collins
:date: November 15, 2024
"""
import os
from pathlib import Path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression, EnvironmentVariable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


# Define the arguments for the XACRO file
ARGUMENTS = [
    DeclareLaunchArgument('robot_name', default_value=EnvironmentVariable("ROBOT_MODEL"),
                          description='Name of the robot'),
    DeclareLaunchArgument('prefix', default_value='',
                          description='Prefix for robot joints and links'),
    DeclareLaunchArgument('add_world', default_value='true',
                          choices=['true', 'false'],
                          description='Whether to add world link'),
    DeclareLaunchArgument('base_link', default_value='base_link',
                          description='Name of the base link'),
    DeclareLaunchArgument('base_type', default_value='g_shape',
                          description='Type of the base'),
    DeclareLaunchArgument('flange_link', default_value='link6_flange',
                          description='Name of the flange link'),
    DeclareLaunchArgument('gripper_type', default_value='adaptive_gripper',
                          description='Type of the gripper'),
    DeclareLaunchArgument('use_camera', default_value='false',
                          choices=['true', 'false'],
                          description='Whether to use the RGBD Gazebo plugin for point cloud'),
    DeclareLaunchArgument('use_gazebo', default_value='false',
                          choices=['true', 'false'],
                          description='Whether to use Gazebo simulation'),
    DeclareLaunchArgument('use_gripper', default_value='true',
                          choices=['true', 'false'],
                          description='Whether to attach a gripper')
]


def generate_launch_description():
    """Generate the launch description for the mycobot robot visualization.

    This function sets up all necessary nodes and parameters for visualizing
    the mycobot robot in RViz, including:
    - Robot state publisher for broadcasting transforms
    - Joint state publisher for simulating joint movements
    - RViz for visualization

    Returns:
        LaunchDescription: Complete launch description for the visualization setup
    """
    # Define filenames
    urdf_package = 'mycobot_description'

    # Set paths to important files
    pkg_share_description = FindPackageShare(urdf_package)

    # Launch configuration variables
    jsp_gui = LaunchConfiguration('jsp_gui')

    # Declare the launch arguments
    declare_jsp_gui_cmd = DeclareLaunchArgument(
        name='jsp_gui',
        default_value='true',
        choices=['true', 'false'],
        description='Flag to enable joint_state_publisher_gui')

    urdf_model_filename = PythonExpression(
        ["'", EnvironmentVariable("ROBOT_MODEL"), "' + '.urdf.xacro'"])
    urdf_model_path = PathJoinSubstitution(
        [pkg_share_description, 'urdf', 'robots', urdf_model_filename])
    rviz_config_robot_only_path = PathJoinSubstitution(
        [pkg_share_description, 'rviz', 'mycobot_description_only.rviz'])

    robot_description_content = ParameterValue(Command([
        'xacro', ' ', urdf_model_path, ' ',
        'robot_name:=', LaunchConfiguration('robot_name'), ' ',
        'prefix:=', LaunchConfiguration('prefix'), ' ',
        'add_world:=', LaunchConfiguration('add_world'), ' ',
        'base_link:=', LaunchConfiguration('base_link'), ' ',
        'base_type:=', LaunchConfiguration('base_type'), ' ',
        'flange_link:=', LaunchConfiguration('flange_link'), ' ',
        'gripper_type:=', LaunchConfiguration('gripper_type'), ' ',
        'use_camera:=', LaunchConfiguration('use_camera'), ' ',
        'use_gazebo:=', LaunchConfiguration('use_gazebo'), ' ',
        'use_gripper:=', LaunchConfiguration('use_gripper')
    ]), value_type=str)

    # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': False,
            'robot_description': robot_description_content}])

    # Publish the joint state values for the non-fixed joints in the URDF file.
    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': False}],
        condition=UnlessCondition(jsp_gui))

    # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    start_joint_state_publisher_gui_cmd = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters=[{'use_sim_time': False}],
        condition=IfCondition(jsp_gui))


    # Launch RViz in base_link coordinates with only the robot
    start_rviz_robot_only_cmd = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_robot_only_path],
        parameters=[{'use_sim_time': False}])

    # Create the launch description and populate
    ld = LaunchDescription(ARGUMENTS)

    # Declare the launch options
    ld.add_action(declare_jsp_gui_cmd)

    # Add any actions
    ld.add_action(start_joint_state_publisher_cmd)
    ld.add_action(start_joint_state_publisher_gui_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_rviz_robot_only_cmd)

    return ld
