from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from xacro import process_file
import os

def generate_launch_description():
    pkg_clase3 = get_package_share_directory('clase3')  # Ruta a tu paquete
    controllers_file = os.path.join(pkg_clase3, 'config', 'ros2_controllers.yaml')
    
    #urdf_file = os.path.join(pkg_clase3, 'urdf', 'double_pendulum.urdf')
    xacro_file = os.path.join(pkg_clase3, 'urdf', 'double_pendulum.xacro')
    urdf_content = process_file(xacro_file).toxml()
    urdf_file = os.path.join(pkg_clase3, 'urdf', 'double_pendulum.xacro')
    #urdf_file = '/tmp/double_pendulum.urdf'
    #with open(urdf_file, 'w') as f:
    #    f.write(urdf_content)

    # Lanzar Gazebo Sim (Ignition) en ROS 2 Jazzy
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
        )]),
    )

         
         
    # Gazebo bridge
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        output="screen",
    )
    
    # Bridge para comunicación ROS 2 <-> Gazebo
    #bridge = Node(
    #    package='ros_gz_bridge',
    #    executable='parameter_bridge',
    #    arguments=[
    #        '/model/double_pendulum/joint_state@sensor_msgs/msg/JointState@gz.msgs.Model',
    #        '/world/default/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
    #    ],
    #    output='screen'
    #)
    
    # Robot State Publisher (necesario para que ROS 2 publique el estado del robot)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': urdf_content}]
    )
    
    # Sliders para modificar /joint_states
    joint_state_publisher_gui = Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
    )
         

    
    # Spawn del modelo en Gazebo Sim
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            "-topic",
            "/robot_description",
            "-name", "double_pendulum",
            "rrbot_system_position",
            "-allow_renaming",
            "true",
        ],
        output='screen'
    )

    # Lanzar controlador de ROS 2
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controllers_file]
    )
    
    # Activar controladores después de iniciar la simulación
    load_effort_controller = ExecuteProcess(
        cmd=["ros2", "control", "load_controller", "--set-state", "active", "effort_controller"],
        output="screen"
    )   
    
    return LaunchDescription([
        gazebo,                  # Inicia Gazebo Sim
        bridge,                  # Agrega el bridge para comunicación con ROS 2
        robot_state_publisher,   # Publica estado del robot en ROS 2
        joint_state_publisher_gui,
        spawn_entity,            # Spawnea el modelo en Gazebo
        controller_manager,       # Inicia ros2_control
        #load_effort_controller,   # Carga el controlador de esfuerzo        
    ])

