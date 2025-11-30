# digital_twin_hallway

A minimal ROS 2 + Gazebo digital twin of a hallway. Includes:
- Xacro URDF describing a hallway (floor, two walls, ceiling)
- Gazebo world that spawns the URDF into the environment
- A launch file to start Gazebo and spawn the hallway model
- Example RViz config to visualize TF/camera

Tested with: ROS 2 Humble / Gazebo (use the gazebo_ros launch available in your ROS distro).

## Quick start (local)

1. Clone or create this repo locally:
   ```bash
   git clone <your-repo-url>
   cd digital_twin_hallway
