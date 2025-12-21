# Hallway Digital Twin

A minimal, parametric **ROS 2 + Gazebo** digital twin of a hallway environment. This project provides a foundational corridor world designed for testing mobile robot navigation, SLAM, and sensor integration in a controlled simulation.

[![Digital Twin Hallway Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

The **Digital Twin** is designed to facilitate "Simulation-to-Reality" (Sim2Real) workflows. Unlike static meshes, this project utilizes **Xacro (XML Macros)** to define the environment. This allows you to:

* **Parameterize Dimensions:** Easily change hallway length, width, or height by editing variables in the Xacro file.
* **Sensor Testing:** The environment is optimized for LiDAR and Camera plugins to ensure realistic ray-tracing and physics.
* **Lightweight Simulation:** High-fidelity visuals with low computational overhead, making it ideal for testing navigation stacks.

## Prerequisites

| Requirement | Specification |
| :--- | :--- |
| **Operating System** | Ubuntu 22.04 (Jammy Jellyfish) |
| **ROS 2 Distro** | Humble Hawksbill |
| **Gazebo** | Gazebo 11 (Classic) |
| **Build Tool** | Colcon |

## Setup Guide

Follow these steps to build and launch the environment on your local machine.

### 1. Create a Workspace
If you don't have a workspace set up, create one:
```bash
mkdir -p ~/hallway_ws/src
cd ~/hallway_ws/src
```

### 2. Clone the Repository
```bash
git clone https://github.com/rueyday/hallway-digital-twin.git
```

### 3. Install Dependencies
Ensure you have the necessary ROS 2 packages for Gazebo and Xacro:
```bash
cd ~/hallway_ws
rosdep install -i --from-path src --rosdistro humble -y
```

### 4. Build and Source
```bash
colcon build --symlink-install
source install/setup.bash
```

### 5. Running the Simulation
Launch the Hallway
To start Gazebo, spawn the hallway model, and publish the robot state:
```bash
ros2 launch digital_twin_hallway hallway.launch.py
```

### 6. Visualize in RViz
To see the TF tree and sensor frames, run:
```bash
ros2 run rviz2 rviz2 -d src/digital_twin_hallway/config/hallway_config.rviz
```
## Project Structure
```bash
digital_twin_hallway/
├── config/             # RViz configuration files
├── launch/             # Python launch files
├── urdf/               # Xacro files (hallway geometry)
├── worlds/             # Gazebo .world files
├── CMakeLists.txt      # Build instructions
└── package.xml         # Package metadata
```
