# Hallway Digital Twin

A minimal, parametric **ROS 2 + Gazebo** digital twin of a hallway environment. This project provides a foundational corridor world designed for testing mobile robot navigation, SLAM, and sensor integration in a controlled simulation.

<p align="center">
  <img src="demo.gif" width="45%">
</p>
<tr>
  <td align="center" width="50%">
    <a href="https://www.youtube.com/watch?v=RyhKSUHeHf8">
      <b>Full Demo Video (YouTube)</b>
    </a>
   </td>
</tr>

## Prerequisites

| Requirement | Specification |
| :--- | :--- |
| **Operating System** | Ubuntu 24.04 |
| **ROS 2 Distro** | Rolling |
| **Gazebo** | Gazebo Ionic |
| **Build Tool** | Colcon |

## Setup Guide

Follow these steps to build and launch the environment on your local machine.

If you don't have a workspace set up, create one:
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Clone the Repository
```bash
git clone https://github.com/rueyday/hallway-digital-twin.git
```

Build and Source
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Launch the Hallway
To start Gazebo, spawn the hallway model, and publish the robot state:
```bash
ros2 launch hallway-digital-twin digital_twin.launch.py
```

### Test Drive the Robot and visualize LiDAR Data

Use the provided test drive script to control the robot:

```bash
python ~/ros2_ws/src/hallway-digital-twin/scripts/test_drive.py
```

Run the LiDAR visualization node:

```bash
python ~/ros2_ws/src/hallway-digital-twin/scripts/lidar_visualization.py
```

## Project Structure

```
hallway-digital-twin/
├── launch/                     # Launch files
│   └── digital_twin.launch.py  # Main launch file
├── urdf/                       # Robot and environment descriptions
│   └── *.xacro                 # Xacro model files
├── worlds/                     # Gazebo world files
│   └── hallway_world.sdf       # Main hallway world
├── scripts/                    # Python scripts
│   ├── test_drive.py           # Robot control test
│   └── lidar_visualization.py  # LiDAR data visualizer
├── CMakeLists.txt              # Build configuration
├── package.xml                 # Package metadata
└── README.md                   # This file
```
