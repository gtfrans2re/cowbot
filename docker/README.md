# Docker Simulation Setup

Quick reference for running Gazebo and RViz simulation in Docker.

## Quick Start

```bash
cd ~/cowbot/docker

# Build image (first time: 15-30 min)
docker compose build

# Launch simulation
docker compose run --rm cowbot-simulation \
    bash -c "colcon build --symlink-install && \
             source install/setup.bash && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

## Prerequisites

1. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Configure X11:**
   ```bash
   xhost +local:docker
   export DISPLAY=:0
   echo "xhost +local:docker" >> ~/.bashrc
   echo "export DISPLAY=:0" >> ~/.bashrc
   ```

## Common Commands

```bash
# Interactive shell
docker compose run --rm cowbot-simulation bash

# Build workspace inside container
docker compose run --rm cowbot-simulation \
    bash -c "colcon build --symlink-install"

# Launch simulation
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"

# View logs
docker compose logs -f

# Stop container
docker compose down
```

## Troubleshooting

**GPU device driver error:**
- Already fixed in `docker-compose.yml` (GPU deploy section removed)

**Duplicate packages error:**
- Fixed: Dockerfile no longer copies workspace
- Rebuild: `docker compose build --no-cache`

**X11 errors:**
```bash
xhost +local:docker
export DISPLAY=:0
```

**Build fails:**
- Check if `gz-jazzy` package exists: `apt-cache search gz-jazzy`
- ROS 2 Jazzy uses Ignition Gazebo (`gz-jazzy`), not `ros-jazzy-gazebo-*` packages

For complete documentation, see: `../README.md`
