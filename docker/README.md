# Docker Simulation Setup - Complete Guide

## Your System Specs

- **RAM**: 32GB ✅ (Perfect for Docker!)
- **CPU**: Intel Core Ultra 5 125H × 18 ✅ (Excellent!)
- **GPU**: Intel Arc Graphics ✅
- **Disk**: 1TB ✅ (Plenty of space)
- **OS**: Ubuntu 24.04.3 LTS ✅

## Prerequisites

### 1. Install Docker

```bash
# Remove old versions if any
sudo apt-get remove docker docker-engine docker.io containerd runc

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and log back in for group changes to take effect
# Or run: newgrp docker
```

**Verify installation:**
```bash
docker --version
docker ps
```

### 2. Install Docker Compose

```bash
# Docker Compose V2 (included with Docker Desktop, or install separately)
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Verify
docker compose version
```

### 3. Configure X11 for GUI (Important!)

**For Wayland (your system):**

```bash
# Allow X11 connections
xhost +local:docker

# Make it persistent (add to ~/.bashrc)
echo "xhost +local:docker" >> ~/.bashrc
```

**Alternative for Wayland:**
```bash
# If using Wayland, you might need XWayland
# Check if it's installed
echo $XDG_SESSION_TYPE

# For Wayland, ensure XWayland is running
```

### 4. Set Up ROS 2 Environment Variables

Create `docker/.env` file:
```bash
cd ~/cowbot/docker
cat > .env << EOF
ROS_DOMAIN_ID=0
DISPLAY=${DISPLAY:-:0}
XAUTHORITY=${XAUTHORITY:-${HOME}/.Xauthority}
EOF
```

## Build Docker Image

### Step 1: Navigate to Docker Directory

```bash
cd ~/cowbot/docker
```

### Step 2: Build the Image

```bash
# Build the Docker image (this may take 15-30 minutes)
docker compose build

# Or build without cache
docker compose build --no-cache
```

**What happens:**
- Downloads ROS 2 Jazzy desktop image (~3GB)
- Installs Gazebo, RViz, and all dependencies
- Builds your workspace inside the container

### Step 3: Verify Build

```bash
docker images | grep cowbot-simulation
```

Should show: `cowbot-simulation:jazzy`

## Running Simulation

### Option 1: Interactive Container (Recommended for First Time)

```bash
cd ~/cowbot/docker

# Start container in interactive mode
docker compose run --rm cowbot-simulation bash

# Inside container:
source /ros2_ws/install/setup.bash
colcon build --symlink-install  # Build workspace
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py
```

### Option 2: Direct Launch (Quick Start)

```bash
cd ~/cowbot/docker

# Launch simulation directly
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             colcon build --symlink-install && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

### Option 3: Detached Background (For Long Sessions)

```bash
cd ~/cowbot/docker

# Start container in background
docker compose up -d

# Execute commands in running container
docker compose exec cowbot-simulation bash -c \
    "source /ros2_ws/install/setup.bash && \
     ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"

# View logs
docker compose logs -f

# Stop container
docker compose down
```

## Network Bridge with RPi

### Setup on Local Machine (Docker Container)

The container uses `network_mode: host`, so it can communicate directly with your RPi.

**Inside container:**
```bash
# Set ROS domain (already set in docker-compose.yml)
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0

# Verify you can see RPi topics
ros2 topic list
```

### Setup on RPi

**On RPi (`~/.bashrc`):**
```bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
```

**Test connection:**
```bash
# On RPi
ros2 run demo_nodes_cpp talker

# In Docker container
ros2 topic echo /chatter
```

## Common Commands

### Build Commands

```bash
# Rebuild image
docker compose build

# Rebuild without cache
docker compose build --no-cache

# Rebuild specific service
docker compose build cowbot-simulation
```

### Run Commands

```bash
# Interactive shell
docker compose run --rm cowbot-simulation bash

# Run specific command
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && ros2 topic list"

# Start in background
docker compose up -d

# Stop container
docker compose down
```

### Debug Commands

```bash
# View logs
docker compose logs -f

# View logs from specific service
docker compose logs -f cowbot-simulation

# Execute command in running container
docker compose exec cowbot-simulation bash

# Check container status
docker compose ps

# Inspect container
docker compose exec cowbot-simulation env
```

### Cleanup Commands

```bash
# Stop and remove containers
docker compose down

# Remove volumes (careful - deletes data!)
docker compose down -v

# Remove image
docker rmi cowbot-simulation:jazzy

# Clean up all Docker resources (use with caution!)
docker system prune -a
```

## Troubleshooting

### Problem: Cannot connect to X server

**Solution:**
```bash
# Allow X11 connections
xhost +local:docker

# Verify DISPLAY is set
echo $DISPLAY

# Check XAUTHORITY
echo $XAUTHORITY
```

### Problem: Gazebo GUI not showing

**Solution:**
```bash
# Check X11 forwarding
docker compose exec cowbot-simulation env | grep DISPLAY

# Try running headless mode first
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py headless:=true"
```

### Problem: Container can't see RPi topics

**Solution:**
- Verify `network_mode: host` in docker-compose.yml
- Check ROS_DOMAIN_ID matches on both machines
- Ensure firewall allows ROS 2 ports (7400-7500 UDP, 11311 TCP)

### Problem: Out of disk space

**Solution:**
```bash
# Check Docker disk usage
docker system df

# Clean up unused images
docker image prune -a

# Clean up build cache
docker builder prune
```

### Problem: Build fails

**Solution:**
```bash
# Check build logs
docker compose build 2>&1 | tee build.log

# Rebuild from scratch
docker compose build --no-cache --pull
```

### Problem: GPU not working

**Solution:**
- Intel Arc GPU support in Docker is experimental
- Gazebo can run without GPU (slower but functional)
- Check GPU drivers:
```bash
lspci | grep -i vga
dmesg | grep -i intel
```

## Performance Tips

### 1. Resource Allocation

Your system has plenty of resources, but you can limit if needed:

Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '16'  # Use 16 of 18 cores
      memory: 16G  # Use 16GB of 32GB
```

### 2. Build Optimization

```bash
# Use build cache
docker compose build

# Parallel builds (if multiple services)
docker compose build --parallel
```

### 3. Volume Mounting

The workspace is mounted as a volume, so changes on host are immediately available in container (no rebuild needed).

### 4. Persistent Data

Data in Docker volumes persists between container restarts:
- `gazebo_models` - Downloaded Gazebo models
- `gazebo_worlds` - World files
- `simulation_data` - Simulation output data

## Workflow Examples

### Example 1: First-Time Setup

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# 2. Configure X11
xhost +local:docker
echo "xhost +local:docker" >> ~/.bashrc

# 3. Build image
cd ~/cowbot/docker
docker compose build

# 4. Test launch
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             colcon build --symlink-install && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

### Example 2: Daily Development

```bash
cd ~/cowbot/docker

# Quick launch
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"

# Or interactive session
docker compose run --rm cowbot-simulation bash
```

### Example 3: Testing Changes

```bash
# Edit code on host machine
vim ~/cowbot/cowbot_ws/src/cowbot_navigation/...

# Rebuild in container
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             colcon build --packages-select cowbot_navigation && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

## Next Steps

1. ✅ Install Docker
2. ✅ Build Docker image
3. ✅ Configure X11
4. ✅ Launch simulation
5. ✅ Test network bridge with RPi
6. ✅ Start developing!

For network bridge setup, see: `../ROS2_NETWORK_BRIDGE.md`

