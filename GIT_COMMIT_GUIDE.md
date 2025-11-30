# Git Commit and Push Guide

## ✅ Files Already Staged

All Docker and simulation files have been added to git:

### Docker Files
- `docker/Dockerfile`
- `docker/docker-compose.yml`
- `docker/entrypoint.sh`
- `docker/.dockerignore`
- `docker/README.md`
- `docker/QUICK_START.md`

### Documentation
- `DOCKER_COMPLETE_SETUP.md`
- `DOCKER_SETUP_SUMMARY.md`
- `DOCKER_SIMULATION_SETUP.md`
- `SIMULATION_COMPLETE_GUIDE.md`
- `SIMULATION_QUICK_REFERENCE.md`
- `SIMULATION_SETUP.md`
- `ROS2_NETWORK_BRIDGE.md`

### Simulation Files
- `cowbot_ws/src/cowbot_gazebo/launch/simulation_with_rviz.launch.py`
- `cowbot_ws/src/cowbot_gazebo/rviz/simulation.rviz`
- `cowbot_ws/src/cowbot_gazebo/worlds/botbox_warehouse.world`
- `cowbot_ws/src/cowbot_gazebo/CMakeLists.txt` (updated)

### Updated Files
- `.gitignore` (added system file ignores)

---

## 🚀 Commit and Push

### Step 1: Review What's Being Committed

```bash
cd ~/cowbot
git status
```

### Step 2: Commit Changes

```bash
git commit -m "Add Docker simulation setup and Gazebo+RViz launch files

- Add complete Docker setup for local machine simulation
  - Dockerfile with ROS 2 Jazzy + Gazebo + RViz
  - docker-compose.yml with host networking
  - Comprehensive documentation

- Add simulation launch files
  - simulation_with_rviz.launch.py (complete Gazebo+RViz launch)
  - RViz configuration (simulation.rviz)
  - World file (botbox_warehouse.world)

- Add documentation
  - Docker setup guides (DOCKER_COMPLETE_SETUP.md, etc.)
  - Simulation guides (SIMULATION_COMPLETE_GUIDE.md, etc.)
  - Network bridge guide (ROS2_NETWORK_BRIDGE.md)

- Update CMakeLists.txt to install rviz and worlds directories
- Update .gitignore to exclude system files"
```

### Step 3: Push to GitHub

```bash
# Push to your repository
git push origin main

# Or if your branch is named differently:
git push origin master
# or
git push origin <your-branch-name>
```

### Step 4: Verify Push

```bash
# Check remote status
git remote -v

# View recent commits
git log --oneline -5
```

---

## 📋 Quick Commit Commands

### Option 1: Single Commit (Recommended)

```bash
cd ~/cowbot
git commit -m "Add Docker simulation setup with Gazebo and RViz"
git push origin main
```

### Option 2: Multiple Commits

```bash
cd ~/cowbot

# Commit Docker files
git commit -m "Add Docker simulation setup" docker/ DOCKER*.md

# Commit simulation files
git commit -m "Add Gazebo and RViz launch files" cowbot_ws/src/cowbot_gazebo/

# Commit documentation
git commit -m "Add simulation and network bridge documentation" SIMULATION*.md ROS2_NETWORK_BRIDGE.md

# Push all commits
git push origin main
```

---

## 🖥️ Clone on Local Machine

After pushing, clone on your local machine:

### Step 1: Clone Repository

```bash
# On your local machine
cd ~
git clone <your-repo-url> cowbot
cd cowbot
```

### Step 2: Checkout Branch (if needed)

```bash
# If you're on a different branch
git checkout <branch-name>
```

### Step 3: Verify Files

```bash
# Check Docker files exist
ls -la docker/

# Check documentation exists
ls -la DOCKER*.md SIMULATION*.md

# Check simulation files exist
ls -la cowbot_ws/src/cowbot_gazebo/launch/simulation_with_rviz.launch.py
ls -la cowbot_ws/src/cowbot_gazebo/rviz/
ls -la cowbot_ws/src/cowbot_gazebo/worlds/
```

### Step 4: Follow Docker Setup Guide

```bash
# Read the complete setup guide
cat DOCKER_COMPLETE_SETUP.md

# Or quick start
cat docker/QUICK_START.md
```

---

## 🔄 Workflow Summary

**On RPi (current machine):**
1. ✅ Files staged
2. Commit changes
3. Push to GitHub

**On Local Machine:**
1. Clone repository
2. Follow `DOCKER_COMPLETE_SETUP.md`
3. Build Docker image
4. Launch simulation

---

## 📝 Commit Message Template

Use this template for detailed commit messages:

```
Add Docker simulation setup and Gazebo+RViz launch files

Features:
- Complete Docker environment for simulation
- Gazebo + RViz launch configuration
- Network bridge capability with RPi
- Comprehensive documentation

Files Added:
- docker/ directory with Dockerfile, compose, and scripts
- Simulation launch files and configurations
- Multiple documentation guides

This enables running simulation on local machine while
bridging with RPi hardware over ROS 2 network.
```

---

## ✅ Verification Checklist

Before pushing, verify:
- [ ] All Docker files are in `docker/` directory
- [ ] All documentation files are at root level
- [ ] Simulation launch files are in workspace
- [ ] No sensitive data in files (API keys, passwords)
- [ ] `.gitignore` excludes build artifacts
- [ ] All files are staged (check with `git status`)

---

## 🐛 Troubleshooting

### Problem: Push rejected

**Solution:**
```bash
# Pull latest changes first
git pull origin main --rebase

# Resolve conflicts if any, then push
git push origin main
```

### Problem: Files not appearing in repo

**Solution:**
```bash
# Verify files are tracked
git ls-files | grep docker
git ls-files | grep DOCKER

# Re-add if needed
git add docker/ DOCKER*.md
git commit -m "Add Docker files"
git push origin main
```

### Problem: Want to undo staging

**Solution:**
```bash
# Unstage specific file
git reset HEAD <file>

# Unstage all files
git reset HEAD
```

---

## 🎯 Next Steps

1. **Commit and push** (commands above)
2. **Clone on local machine**
3. **Follow** `DOCKER_COMPLETE_SETUP.md`
4. **Start simulating!**

