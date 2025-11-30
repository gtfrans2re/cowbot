#!/bin/bash
# ============================================================================
# COPY-PASTE COMMANDS FOR DOCKER BUILD FIX
# ============================================================================

echo "==================================================================="
echo "Step 1: Test if Gazebo is in base image"
echo "==================================================================="
echo ""
echo "Run this command:"
echo "docker run -it --rm osrf/ros:jazzy-desktop-full which gz"
echo ""
read -p "Press Enter to continue..."

echo ""
echo "==================================================================="
echo "Step 2: Try building with fixed Dockerfile"
echo "==================================================================="
echo ""
echo "Run these commands:"
echo "cd ~/cowbot/docker"
echo "docker compose build"
echo ""
read -p "Press Enter to continue..."

echo ""
echo "==================================================================="
echo "If build fails, check available packages:"
echo "==================================================================="
echo ""
echo "docker run -it --rm osrf/ros:jazzy-desktop-full bash -c \"apt-get update && apt-cache search gz-jazzy | head -20\""
echo ""

