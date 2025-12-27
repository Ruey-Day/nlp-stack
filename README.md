# Hallway Digital Twin

A high-fidelity Simulation-to-Reality (Sim2Real) environment for **ROS 2 Rolling**. This project features a parameterized hallway with heterogeneous wall materials and a differential drive robot equipped with a GPU-accelerated LiDAR.

## 📁 Project Structure

```text
.
├── CMakeLists.txt          # Build system configuration
├── config
│   └── rviz_hallway.rviz   # Pre-configured RViz2 display settings
├── launch
│   └── digital_twin.launch.py # Main launch (Gazebo Sim + RViz + Bridge)
├── package.xml             # Dependencies and metadata
├── README.md               # Documentation
├── test_drive.py           # Custom keyboard teleop controller
├── urdf
│   └── robot.urdf.xacro    # Parameterized environment and robot URDF
└── worlds
    └── hallway_world.sdf   # Gazebo Sim world configuration