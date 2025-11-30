# Docker Quick Start Guide

## 🚀 Fastest Way to Get Started

### Step 1: Install Docker (One-time setup)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Configure X11

```bash
xhost +local:docker
echo "xhost +local:docker" >> ~/.bashrc
export DISPLAY=:0
echo "export DISPLAY=:0" >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Build Docker Image

```bash
cd ~/cowbot/docker
docker compose build
```

**Takes 15-30 minutes on first build** ⏱️

### Step 4: Launch Simulation

```bash
cd ~/cowbot/docker
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             colcon build --symlink-install && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

## ✅ Done!

Gazebo and RViz should now open on your screen!

## 🛠️ Common Commands

### Launch Simulation
```bash
cd ~/cowbot/docker
docker compose run --rm cowbot-simulation \
    bash -c "source /ros2_ws/install/setup.bash && \
             ros2 launch cowbot_gazebo simulation_with_rviz.launch.py"
```

### Interactive Shell
```bash
cd ~/cowbot/docker
docker compose run --rm cowbot-simulation bash
```

### View Logs
```bash
docker compose logs -f
```

### Stop Container
```bash
docker compose down
```

## 📚 Full Documentation

- **DOCKER_COMPLETE_SETUP.md** - Complete step-by-step guide
- **docker/README.md** - Detailed Docker documentation

## 🐛 Problems?

**X11 errors?**
```bash
xhost +local:docker
export DISPLAY=:0
```

**Build fails?**
```bash
docker compose build --no-cache
```

**Can't see GUI?**
- Check DISPLAY is set: `echo $DISPLAY`
- Verify X11 forwarding: `xhost`

For more help, see: **DOCKER_COMPLETE_SETUP.md**

