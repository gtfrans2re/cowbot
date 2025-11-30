# Complete Docker Simulation Setup Guide

## 🎯 Quick Start

**Your Machine**: 32GB RAM, 18-core CPU, 1TB disk - Perfect for Docker! ✅

This guide walks you through setting up Gazebo + RViz simulation in Docker containers.

---

## Step 1: Install Docker

### Install Docker Engine

```bash
# Remove old versions (if any)
sudo apt-get remove docker docker-engine docker.io containerd runc

# Install Docker using official script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Apply group changes (or log out/in)
newgrp docker

# Verify installation
docker --version
docker ps
```

**Expected output:**
```
Docker version 24.x.x or higher
```

### Install Docker Compose

```bash
# Install Docker Compose plugin
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Verify
docker compose version
```

---

## Step 2: Configure X11 Display (For GUI)

Your system uses **Wayland**, so we need to configure X11 forwarding:

```bash
# Allow Docker containers to access X server
xhost +local:docker

# Make it permanent (add to ~/.bashrc)
echo "xhost +local:docker" >> ~/.bashrc
source ~/.bashrc

# Verify DISPLAY is set
echo $DISPLAY
```

**Note**: If `DISPLAY` is empty, you may need to export it:
```bash
export DISPLAY=:0
echo "export DISPLAY=:0" >> ~/.bashrc
```

---

## Step 3: Prepare Docker Files

All Docker files are already created in `~/cowbot/docker/`. Let's verify:

```bash
cd ~/cowbot
ls -la docker/
```

You should see:
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Container orchestration
- `entrypoint.sh` - Startup script
- `README.md` - Detailed documentation

---

## Step 4: Build Docker Image

```bash
cd ~/cowbot/docker

# Build the image (takes 15-30 minutes, downloads ~3GB)
docker compose build

# Watch the build process - it will:
# 1. Download ROS 2 Jazzy desktop image
# 2. Install Gazebo (gz-jazzy) and RViz dependencies
# 3. Build your workspace
```

**Note:** If the build fails with package errors, check `docker/BUILD_TROUBLESHOOTING.md` for solutions.

**What to expect:**
- First build: 15-30 minutes (downloads base image)
- Subsequent builds: 5-10 minutes (uses cache)
- Disk space needed: ~5-10GB for images

**Troubleshooting build issues:**
```bash
# If build fails, see full logs
docker compose build 2>&1 | tee build.log

# Rebuild from scratch
docker compose build --no-cache
```

---

## Step 5: Verify Build

```bash
# Check image was created
docker images | grep cowbot-simulation

# Should show:
# cowbot-simulation   jazzy   <image-id>   <time>   <size>
```

---

## Step 6: Test Container

### Option A: Interactive Shell (Recommended for first test)

```bash
cd ~/cowbot/docker

# Start container interactively
docker compose run --rm cowbot-simulation bash

# Inside container, test ROS 2:
source /ros2_ws/install/setup.bash
ros2 --help
ros2 pkg list | grep cowbot

# Test workspace build:
colcon build --symlink-install

# Exit container
exit
```

### Option B: Quick Test Launch

```bash
cd ~/cowbot/docker

# Test if Gazebo can start (headless mode first)
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             colcon build --symlink-install && \
             gz --version"
```

---

## Step 7: Launch Simulation

### Launch Gazebo + RViz

```bash
cd ~/cowbot/docker

# Launch complete simulation
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             colcon build --symlink-install && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

**What should happen:**
1. ✅ Container starts
2. ✅ Workspace builds
3. ✅ Gazebo window opens (with robot)
4. ✅ RViz window opens (with visualizations)

**If GUI doesn't show:**
```bash
# Check X11 forwarding
xhost +local:docker
export DISPLAY=:0

# Try headless mode first
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py headless:=true"
```

---

## Step 8: Network Bridge with RPi (Optional)

To connect simulation with your RPi hardware:

### On Your Local Machine (Host)

The Docker container uses `network_mode: host`, so it shares your host's network.

**Verify network setup:**
```bash
# Check ROS domain ID in container
docker compose run --rm cowbot-simulation env | grep ROS_DOMAIN_ID

# Should show: ROS_DOMAIN_ID=0
```

### On RPi

```bash
# Add to ~/.bashrc
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0

# Reload
source ~/.bashrc
```

### Test Connection

**On RPi:**
```bash
ros2 run demo_nodes_cpp talker
```

**In Docker container (new terminal):**
```bash
cd ~/cowbot/docker
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             ros2 topic echo /chatter"
```

If you see messages, **network bridge is working!** 🎉

---

## Daily Usage Workflow

### Quick Launch (After Initial Setup)

```bash
cd ~/cowbot/docker
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

### Interactive Development Session

```bash
cd ~/cowbot/docker

# Start interactive container
docker compose run --rm cowbot-simulation bash

# Inside container:
source /ros2_ws/install/setup.bash

# Edit code on host machine (in another terminal)
# Changes are immediately available in container (volume mount)

# Rebuild specific package
colcon build --packages-select cowbot_navigation

# Launch simulation
ros2 launch cowbot_gazebo simulation_with_rviz.launch.py

# Run other commands
ros2 topic list
ros2 node list
ros2 param list
```

### Background Session (Long-running)

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

# Stop when done
docker compose down
```

---

## Useful Commands

### Container Management

```bash
# List running containers
docker compose ps

# View logs
docker compose logs -f

# Stop container
docker compose down

# Remove everything (careful!)
docker compose down -v
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi cowbot-simulation:jazzy

# Clean up unused images
docker image prune -a
```

### Workspace Commands (Inside Container)

```bash
# Build all packages
colcon build --symlink-install

# Build specific package
colcon build --packages-select cowbot_navigation

# Source workspace
source /ros2_ws/install/setup.bash

# List packages
ros2 pkg list | grep cowbot
```

---

## Troubleshooting

### Problem: Docker permission denied

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or use sudo (not recommended for daily use)
sudo docker compose ...
```

### Problem: X11 display errors

**Solution:**
```bash
# Allow Docker access
xhost +local:docker

# Set DISPLAY
export DISPLAY=:0

# Check XAUTHORITY
ls -la ~/.Xauthority
```

### Problem: Container can't see RPi

**Solution:**
- Verify `network_mode: host` in docker-compose.yml
- Check both machines have same ROS_DOMAIN_ID
- Ensure firewall allows ROS 2 ports

### Problem: Out of disk space

**Solution:**
```bash
# Check Docker disk usage
docker system df

# Clean up
docker system prune -a
```

### Problem: Build is slow

**Solution:**
- First build downloads ~3GB, be patient
- Subsequent builds use cache (much faster)
- Consider increasing Docker memory limit

---

## Performance Optimization

### Resource Limits (Optional)

Edit `docker-compose.yml` to limit resources if needed:

```yaml
deploy:
  resources:
    limits:
      cpus: '16'      # Use 16 of 18 cores
      memory: 24G     # Use 24GB of 32GB
    reservations:
      cpus: '8'
      memory: 8G
```

Your system has plenty of resources, so this is optional.

### Build Cache

```bash
# Docker automatically caches layers
# Rebuild is much faster after first build
docker compose build
```

---

## Next Steps

1. ✅ Install Docker
2. ✅ Configure X11
3. ✅ Build image
4. ✅ Launch simulation
5. ✅ Test network bridge (optional)
6. ✅ Start developing!

---

## Summary

With Docker on your powerful machine:
- ✅ Isolated environment (won't affect system)
- ✅ Reproducible setup
- ✅ Easy cleanup
- ✅ No resource constraints (32GB RAM!)
- ✅ GPU support (Intel Arc)

**You're all set!** 🚀

For detailed Docker commands, see: `docker/README.md`
For network bridge details, see: `ROS2_NETWORK_BRIDGE.md`

