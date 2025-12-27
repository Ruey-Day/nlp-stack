import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch_ros.actions import Node
import xacro

def generate_launch_description():    
    # Get package directories
    pkg_path = get_package_share_directory('hallway-digital-twin')
    
    # File paths
    world_file = os.path.join(pkg_path, 'worlds', 'hallway_world.sdf')
    urdf_file = os.path.join(pkg_path, 'urdf', 'robot.urdf.xacro')
    
    # Process URDF
    robot_description_raw = xacro.process_file(urdf_file).toxml()
    
    # Save URDF to temp file for spawning
    temp_urdf = '/tmp/robot_hallway.urdf'
    with open(temp_urdf, 'w') as f:
        f.write(robot_description_raw)
    
    print(f"World file: {world_file}")
    print(f"URDF file: {urdf_file}")
    print(f"Temp URDF: {temp_urdf}")
    
    # Launch Gazebo
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', world_file, '-r'],
        output='screen',
        name='gazebo'
    )
    
    # Spawn robot (delayed to let Gazebo start)
    spawn_robot = ExecuteProcess(
        cmd=[
            'gz', 'service',
            '-s', '/world/hallway_world/create',
            '--reqtype', 'gz.msgs.EntityFactory',
            '--reptype', 'gz.msgs.Boolean',
            '--timeout', '5000',
            '--req', f"sdf_filename: '{temp_urdf}', name: 'mobile_robot', pose: {{position: {{x: -4.0, y: 0.0, z: 0.1}}}}"
        ],
        output='screen',
        name='spawn_robot'
    )
    
    # Delay spawn by 5 seconds
    delayed_spawn = TimerAction(
        period=5.0,
        actions=[spawn_robot]
    )
    
    # Print instructions
    print_instructions = ExecuteProcess(
        cmd=[
            'bash', '-c',
            '''
            sleep 6
            echo ""
            echo "============================================================"
            echo "      ROBOT READY
            echo "============================================================"
            echo ""
            '''
        ],
        output='screen',
        name='instructions'
    )
    
    delayed_instructions = TimerAction(
        period=6.0,
        actions=[print_instructions]
    )
    
    return LaunchDescription([
        gazebo,
        delayed_spawn,
        delayed_instructions,
    ])