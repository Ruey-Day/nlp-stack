#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('digital_twin_hallway')

    xacro_path = os.path.join(pkg_share, 'urdf', 'hallway.urdf.xacro')
    urdf_out = os.path.join(pkg_share, 'urdf', 'hallway.urdf')

    # Convert xacro → urdf
    robot_desc = xacro.process_file(xacro_path).toxml()
    with open(urdf_out, "w") as f:
        f.write(robot_desc)

    world_path = os.path.join(pkg_share, 'worlds', 'hallway_world.sdf')

    # Start Ignition Gazebo
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '4', world_path],
        output='screen'
    )

    # Spawn the hallway model into gz-sim
    spawn = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-name', 'hallway_model',
            '-file', urdf_out,
            '-x', '0', '-y', '0', '-z', '0'
        ],
        output='screen'
    )

    return LaunchDescription([gz_sim, spawn])
