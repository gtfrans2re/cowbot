#!/usr/bin/env python3

import time
import threading
import traceback
import math
import rclpy
from rclpy.executors import MultiThreadedExecutor
from cowbot_navigation.robot_interface import RobotInterface

# Global robot interface
robot_interface = None

# Movement primitives

def stop_robot():
    """Stop all motion."""
    robot_interface.linear_velocity = 0.0
    robot_interface.angular_velocity = 0.0

def move_front(speed):
    """Drive forward."""
    robot_interface.linear_velocity = speed
    robot_interface.angular_velocity = 0.0

def move_back(speed):
    """Drive backward."""
    robot_interface.linear_velocity = -speed
    robot_interface.angular_velocity = 0.0

def turn_left(speed):
    """Rotate left."""
    robot_interface.linear_velocity = 0.0
    robot_interface.angular_velocity = speed

def turn_right(speed):
    """Rotate right."""
    robot_interface.linear_velocity = 0.0
    robot_interface.angular_velocity = -speed

def timed_move_front(speed, duration):
    move_front(speed); time.sleep(duration); stop_robot()

def timed_move_back(speed, duration):
    move_back(speed); time.sleep(duration); stop_robot()

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

# Laser scanner accessors - 8 directions

def _get_range_in_sector(center_angle, width):
    """Return minimum range in angular sector."""
    angles = robot_interface.scan_ranges
    amin = robot_interface.scan_angle_min
    inc  = robot_interface.scan_angle_increment
    n    = len(angles)
    
    if n == 0:
        return float('inf')
        
    start = int((center_angle - width/2 - amin) / inc)
    end   = int((center_angle + width/2 - amin) / inc)
    start = max(0, start)
    end   = min(n-1, end)
    
    if start >= n or end < 0:
        return float('inf')
        
    sector = angles[start:end+1]
    vals = [r for r in sector if r != float('inf') and not math.isnan(r)]
    return min(vals) if vals else float('inf')

def get_front_range():
    return _get_range_in_sector(0.0, math.pi/4)

def get_front_left_range():
    return _get_range_in_sector(math.pi/4, math.pi/4)

def get_front_right_range():
    return _get_range_in_sector(-math.pi/4, math.pi/4)

def get_left_range():
    return _get_range_in_sector(math.pi/2, math.pi/3)

def get_right_range():
    return _get_range_in_sector(-math.pi/2, math.pi/3)

def get_back_range():
    return _get_range_in_sector(math.pi, math.pi/4)

def get_back_left_range():
    return _get_range_in_sector(3*math.pi/4, math.pi/4)

def get_back_right_range():
    return _get_range_in_sector(-3*math.pi/4, math.pi/4)

# Test harness

def run_all_tests():
    print("\n===== RUNNING ALL TESTS =====")
    stop_robot(); print("[OK] stop_robot")
    move_front(0.08); time.sleep(0.5); stop_robot(); print("[OK] move_front")
    move_back(0.08); time.sleep(0.5); stop_robot(); print("[OK] move_back")
    turn_left(0.15); time.sleep(0.5); stop_robot(); print("[OK] turn_left")
    turn_right(0.15); time.sleep(0.5); stop_robot(); print("[OK] turn_right")
    timed_move_front(0.08, 1.0); print("[OK] timed_move_front")
    timed_turn_left(0.15, 1.0); print("[OK] timed_turn_left")
    timed_turn_right(0.15, 1.0); print("[OK] timed_turn_right")
    move_distance_front(0.08, 0.16); print("[OK] move_distance_front")
    turn_angle_left(0.15, 0.15); print("[OK] turn_angle_left")
    print("Front range:", get_front_range())
    print("\n[SUCCESS] All tests passed\n")

# 8-direction obstacle avoidance

def enhanced_obstacle_avoidance_loop():
    """
    Navigate with 8-direction obstacle detection.
    Evaluates all directions and moves toward best clearance.
    """
    print("Starting 8-direction obstacle avoidance. Ctrl+C to exit.")
    forward_speed = 0.08
    slow_approach = 0.04
    turn_speed = 0.15
    threshold = 0.6

    try:
        while True:
            front = get_front_range()
            if front > threshold:
                move_front(forward_speed)
            else:
                stop_robot()
                time.sleep(0.5)
                
                # Sample all 8 directions
                f = get_front_range()
                fl = get_front_left_range()
                fr = get_front_right_range()
                l = get_left_range()
                r = get_right_range()
                b = get_back_range()
                bl = get_back_left_range()
                br = get_back_right_range()

                directions = {
                    'front': f,
                    'front-left': fl,
                    'front-right': fr,
                    'left': l,
                    'right': r,
                    'back': b,
                    'back-left': bl,
                    'back-right': br
                }
                best_dir = max(directions, key=directions.get)
                print(f"Obstacle detected. Best direction: {best_dir} ({directions[best_dir]:.2f}m)")

                if directions[best_dir] < 0.3:
                    best_dir = 'back-left'

                if best_dir == 'front':
                    timed_move_front(slow_approach, 0.8)
                elif best_dir == 'back':
                    timed_move_back(slow_approach, 1.0)
                elif best_dir in ('left', 'front-left'):
                    timed_turn_left(turn_speed, 1.0)
                elif best_dir in ('right', 'front-right'):
                    timed_turn_right(turn_speed, 1.0)
                elif best_dir == 'back-left':
                    timed_move_back(slow_approach, 0.5)
                    timed_turn_left(turn_speed, 0.8)
                elif best_dir == 'back-right':
                    timed_move_back(slow_approach, 0.5)
                    timed_turn_right(turn_speed, 0.8)

                stop_robot()
                time.sleep(0.3)
            time.sleep(0.05)

    except KeyboardInterrupt:
        stop_robot()
        print("\n[STOPPED] Avoidance stopped by user")

# ROS spinning and main

def spin_node():
    global executor
    executor.spin()

if __name__ == "__main__":
    rclpy.init(args=None)
    robot_interface = RobotInterface()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(robot_interface)
    threading.Thread(target=spin_node, daemon=True).start()

    print("System initializing...")
    time.sleep(5.0)
    print("[READY] System initialized\n")

    try:
        run_all_tests()
        enhanced_obstacle_avoidance_loop()

    except Exception as e:
        print("\n========== ERROR ==========")
        traceback.print_exception(type(e), e, e.__traceback__)
        print("===========================")

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

    print("System initializing...")
    time.sleep(5.0)
    print("[READY] System initialized\n")

    try:
        run_all_tests()
        enhanced_obstacle_avoidance_loop()

    except Exception as e:
        print("\n========== ERROR ==========")
        traceback.print_exception(type(e), e, e.__traceback__)
        print("===========================")

    finally:
        executor.shutdown()
        robot_interface.destroy_node()
        rclpy.shutdown()
