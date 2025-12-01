# Bug Fixes for Docker Simulation

## Issues Fixed

### 1. X11 Auth Permission Errors ✓
**Problem**: `/tmp/.docker.xauth` permission denied errors when running Docker scripts

**Cause**: Previous runs left the file owned by root, preventing normal user access

**Solution**: 
- Modified `run_docker_sim.sh` and `run_docker_shell.sh`
- Now removes existing auth file with sudo before recreating it
- Ensures proper permissions each time

**Files Changed**:
- `run_docker_sim.sh`
- `run_docker_shell.sh`

---

### 2. Docker Compose Version Warning ✓
**Problem**: Warning about obsolete `version` attribute in docker-compose.yml

**Cause**: Docker Compose v3.8 version field is deprecated in newer versions

**Solution**: 
- Removed `version: '3.8'` line from docker-compose.yml
- Modern Docker Compose auto-detects version from file format

**Files Changed**:
- `docker-compose.yml`

---

### 3. Robot URDF Missing Name ✓
**Problem**: 
```
Error: No name given for the robot.
Failed to parse robot description using: urdf_xml_parser/URDFXMLParser
robot_state_publisher crashed
```

**Cause**: `<robot>` tag in Xacro file was missing the required `name` attribute

**Solution**: 
- Added `name="cowbot"` attribute to robot tag in cowbot_multi_sim.xacro

**Files Changed**:
- `src/cowbot_description/models/urdf/cowbot_multi_sim.xacro`

---

### 4. Gazebo World File Model References ✓
**Problem**: 
```
Unable to find uri[model://sun]
Unable to find uri[model://ground_plane]
Gazebo server crashed immediately
```

**Cause**: World file referenced Gazebo Classic model database URIs that don't exist in Gazebo Harmonic

**Solution**: 
- Replaced `model://sun` include with direct SDF light definition
- Replaced `model://ground_plane` include with complete SDF ground plane model
- Both now fully defined inline in the world file

**Files Changed**:
- `src/cowbot_gazebo/worlds/botbox_warehouse.world`

**Details**:
- Sun: Now a directional light with proper shadows, diffuse, specular settings
- Ground plane: Complete static model with collision, visual, friction properties

---

## Testing

After these fixes:
1. X11 auth warnings should be gone
2. Docker Compose warning eliminated
3. robot_state_publisher should start successfully
4. Gazebo should load world with proper lighting and ground plane
5. Robot should be spawnable in simulation

## Next Steps

The simulation should now work properly. However, you may still want to:

1. **Convert more world elements** to Gazebo Harmonic format if needed
2. **Add ROS-Gazebo bridge topics** for sensors (camera, lidar) in `src/cowbot_gazebo/config/ros_gz_bridge.yaml`
3. **Test robot spawning** to ensure URDF is fully compatible
4. **Verify sensor data** is properly bridged to ROS topics

## Files Modified Summary

```
docker-compose.yml                                        - Removed obsolete version
run_docker_sim.sh                                        - Fixed X11 auth permissions
run_docker_shell.sh                                      - Fixed X11 auth permissions
src/cowbot_description/models/urdf/cowbot_multi_sim.xacro - Added robot name
src/cowbot_gazebo/worlds/botbox_warehouse.world          - Replaced Classic model refs
```

## Commands to Apply Fixes

```bash
# No need to rebuild Docker image - these are source/config changes
# Just clean and restart simulation

# Clean build artifacts
rm -rf build/ install/ log/

# Run simulation
./run_docker_sim.sh
```
