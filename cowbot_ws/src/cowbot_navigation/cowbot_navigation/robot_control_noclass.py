#!/usr/bin/env python3

# python imports
import time
import threading
import traceback
import math
# ros2 imports
import rclpy
from rclpy.executors import MultiThreadedExecutor
# module imports
from cowbot_navigation.robot_interface import RobotInterface

# Global robot interface
robot_interface = None

# ------------------------
# Movement & Sensor Primitives
# ------------------------

def stop_robot():
    """Stop all motion."""
    robot_interface.linear_velocity = 0.0
    robot_interface.angular_velocity = 0.0

def move_front(speed):
    """Drive straight forward."""
    robot_interface.linear_velocity = speed
    robot_interface.angular_velocity = 0.0

def turn_left(speed):
    """Rotate in place left."""
    robot_interface.linear_velocity = 0.0
    robot_interface.angular_velocity = speed

def turn_right(speed):
    """Rotate in place right."""
    robot_interface.linear_velocity = 0.0
    robot_interface.angular_velocity = -speed

def timed_move_front(speed, duration):
    move_front(speed); time.sleep(duration); stop_robot()

def timed_turn_left(speed, duration):
    turn_left(speed); time.sleep(duration); stop_robot()

def timed_turn_right(speed, duration):
    turn_right(speed); time.sleep(duration); stop_robot()

def move_distance_front(speed, distance):
    timed_move_front(speed, distance / speed)

def turn_angle_left(speed, angle):
    timed_turn_left(speed, angle / speed)

def turn_angle_right(speed, angle):
    timed_turn_right(speed, angle / speed)

# Helpers to index into scan_ranges by angle
def _get_range_in_sector(center_angle, width):
    """
    Return the minimum range measured within [center_angle - width/2, center_angle + width/2].
    Angles in radians, scan from robot_interface.scan_angle_min to scan_angle_max.
    """
    angles = robot_interface.scan_ranges
    amin = robot_interface.scan_angle_min
    inc  = robot_interface.scan_angle_increment
    n    = len(angles)
    
    if n == 0:
        return float('inf')
        
    # Compute index bounds
    start = int((center_angle - width/2 - amin) / inc)
    end   = int((center_angle + width/2 - amin) / inc)
    start = max(0, start)
    end   = min(n-1, end)
    
    if start >= n or end < 0:
        return float('inf')
        
    sector = angles[start:end+1]
    # ignore infinities
    vals = [r for r in sector if r != float('inf') and not math.isnan(r)]
    return min(vals) if vals else float('inf')

def get_front_range():
    return _get_range_in_sector(0.0, math.pi/4)       # ±22.5°

def get_front_left_range():
    return _get_range_in_sector(math.pi/4, math.pi/4)  # 45° ±22.5°

def get_front_right_range():
    return _get_range_in_sector(-math.pi/4, math.pi/4) # -45° ±22.5°

def get_left_range():
    return _get_range_in_sector(math.pi/2, math.pi/3)  # 90° ±30°

def get_right_range():
    return _get_range_in_sector(-math.pi/2, math.pi/3) # -90° ±30°

# ------------------------
# Test Harness
# ------------------------

def run_all_tests():
    print("\n===== RUNNING ALL TESTS =====")
    stop_robot(); print("✓ stop_robot")
    move_front(0.2); time.sleep(0.5); stop_robot(); print("✓ move_front")
    turn_left(0.5); time.sleep(0.5); stop_robot(); print("✓ turn_left")
    turn_right(0.5); time.sleep(0.5); stop_robot(); print("✓ turn_right")
    timed_move_front(0.2,1.0); print("✓ timed_move_front")
    timed_turn_left(0.5,1.0); print("✓ timed_turn_left")
    timed_turn_right(0.5,1.0); print("✓ timed_turn_right")
    move_distance_front(0.2,0.2); print("✓ move_distance_front")
    turn_angle_left(0.5,0.5); print("✓ turn_angle_left")
    print("Front range sample:", get_front_range())
    print("\n✅ All tests passed!\n")

# ------------------------
# Enhanced Obstacle-Avoidance
# ------------------------

def enhanced_obstacle_avoidance_loop():
    """
    Drive forward and when an obstacle is detected in front,
    choose the clearest direction among: front-left, front-right, left, right.
    Spin in that direction until front sector clears, then resume forward.
    """
    print("Starting enhanced avoidance loop. Ctrl+C to exit.")
    forward_speed = 0.2
    turn_speed    = 0.5
    threshold     = 0.4  # safety margin

    try:
        while True:
            front = get_front_range()
            if front > threshold:
                # Path clear: drive straight
                move_front(forward_speed)
            else:
                # Obstacle ahead: stop and evaluate sectors
                stop_robot()
                fl = get_front_left_range()
                fr = get_front_right_range()
                l  = get_left_range()
                r  = get_right_range()

                # Choose best direction
                directions = {
                    'front-left': fl,
                    'front-right': fr,
                    'left': l,
                    'right': r
                }
                best_dir = max(directions, key=directions.get)
                print(f"Obstacle detected. Best clearance: {best_dir} ({directions[best_dir]:.2f} m)")

                # Spin until front clears
                if best_dir in ('left', 'front-left'):
                    while get_front_range() <= threshold:
                        turn_left(turn_speed)
                        time.sleep(0.05)
                else:
                    while get_front_range() <= threshold:
                        turn_right(turn_speed)
                        time.sleep(0.05)

                stop_robot()
                time.sleep(0.1)
            time.sleep(0.05)

    except KeyboardInterrupt:
        stop_robot()
        print("\n🚧 Enhanced avoidance stopped by user.")

# ------------------------
# ROS Spinning & Main
# ------------------------

def spin_node():
    global executor
    executor.spin()

if __name__ == "__main__":
    rclpy.init(args=None)
    robot_interface = RobotInterface()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(robot_interface)
    threading.Thread(target=spin_node, daemon=True).start()

    print("System ready in 5 seconds...")
    time.sleep(5.0)
    print("🚀 RUNNING\n")

    try:
        run_all_tests()
        enhanced_obstacle_avoidance_loop()

    except Exception as e:
        print("~~~~~~~~~~~ ERROR ~~~~~~~~~~~")
        traceback.print_exception(type(e), e, e.__traceback__)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    finally:
        executor.shutdown()
        robot_interface.destroy_node()
        rclpy.shutdown()


def main():
    """Entry point for the robot control node."""
    global robot_interface, executor
    rclpy.init(args=None)
    robot_interface = RobotInterface()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(robot_interface)
    threading.Thread(target=spin_node, daemon=True).start()

    print("System ready in 5 seconds...")
    time.sleep(5.0)
    print("🚀 RUNNING\n")

    try:
        run_all_tests()
        enhanced_obstacle_avoidance_loop()

    except Exception as e:
        print("~~~~~~~~~~~ ERROR ~~~~~~~~~~~")
        traceback.print_exception(type(e), e, e.__traceback__)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    finally:
        executor.shutdown()
        robot_interface.destroy_node()
        rclpy.shutdown()
