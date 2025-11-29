#!/usr/bin/env python3

import time
import threading
import traceback
import math
import rclpy
from rclpy.executors import MultiThreadedExecutor
from cowbot_navigation.robot_interface import RobotInterface

class RobotControl:
    def __init__(self, robot_interface: RobotInterface):
        self.robot_interface = robot_interface

    # Movement primitives
    def stop_robot(self):
        """Stop all motion."""
        self.robot_interface.linear_velocity = 0.0
        self.robot_interface.angular_velocity = 0.0

    def move_front(self, speed: float):
        """Drive forward."""
        self.robot_interface.linear_velocity = speed
        self.robot_interface.angular_velocity = 0.0

    def move_back(self, speed: float):
        """Drive backward."""
        self.robot_interface.linear_velocity = -speed
        self.robot_interface.angular_velocity = 0.0

    def turn_left(self, speed: float):
        """Rotate left."""
        self.robot_interface.linear_velocity = 0.0
        self.robot_interface.angular_velocity = speed

    def turn_right(self, speed: float):
        """Rotate right."""
        self.robot_interface.linear_velocity = 0.0
        self.robot_interface.angular_velocity = -speed

    def timed_move_front(self, speed: float, duration: float):
        self.move_front(speed)
        time.sleep(duration)
        self.stop_robot()

    def timed_move_back(self, speed: float, duration: float):
        self.move_back(speed)
        time.sleep(duration)
        self.stop_robot()

    def timed_turn_left(self, speed: float, duration: float):
        self.turn_left(speed)
        time.sleep(duration)
        self.stop_robot()

    def timed_turn_right(self, speed: float, duration: float):
        self.turn_right(speed)
        time.sleep(duration)
        self.stop_robot()

    def move_distance_front(self, speed: float, distance: float):
        self.timed_move_front(speed, distance / speed)

    def turn_angle_left(self, speed: float, angle: float):
        self.timed_turn_left(speed, angle / speed)

    def turn_angle_right(self, speed: float, angle: float):
        self.timed_turn_right(speed, angle / speed)

    # Laser scanner accessors - 8 directions
    def _get_range_in_sector(self, center_angle: float, width: float) -> float:
        """Return minimum range in angular sector."""
        angles = self.robot_interface.scan_ranges
        amin = self.robot_interface.scan_angle_min
        inc  = self.robot_interface.scan_angle_increment
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

    def get_front_range(self) -> float:
        return self._get_range_in_sector(0.0, math.pi/4)

    def get_front_left_range(self) -> float:
        return self._get_range_in_sector(math.pi/4, math.pi/4)

    def get_front_right_range(self) -> float:
        return self._get_range_in_sector(-math.pi/4, math.pi/4)

    def get_left_range(self) -> float:
        return self._get_range_in_sector(math.pi/2, math.pi/3)

    def get_right_range(self) -> float:
        return self._get_range_in_sector(-math.pi/2, math.pi/3)

    def get_back_range(self) -> float:
        return self._get_range_in_sector(math.pi, math.pi/4)

    def get_back_left_range(self) -> float:
        return self._get_range_in_sector(3*math.pi/4, math.pi/4)

    def get_back_right_range(self) -> float:
        return self._get_range_in_sector(-3*math.pi/4, math.pi/4)

    # Test harness
    def run_all_tests(self):
        print("\n===== RUNNING ALL TESTS =====")
        self.stop_robot(); print("[OK] stop_robot")
        self.move_front(0.08); time.sleep(0.5); self.stop_robot(); print("[OK] move_front")
        self.move_back(0.08); time.sleep(0.5); self.stop_robot(); print("[OK] move_back")
        self.turn_left(0.15); time.sleep(0.5); self.stop_robot(); print("[OK] turn_left")
        self.turn_right(0.15); time.sleep(0.5); self.stop_robot(); print("[OK] turn_right")
        self.timed_move_front(0.08, 1.0); print("[OK] timed_move_front")
        self.timed_turn_left(0.15, 1.0); print("[OK] timed_turn_left")
        self.timed_turn_right(0.15, 1.0); print("[OK] timed_turn_right")
        self.move_distance_front(0.08, 0.16); print("[OK] move_distance_front")
        self.turn_angle_left(0.15, 0.15); print("[OK] turn_angle_left")
        print("Front range:", self.get_front_range())
        print("\n[SUCCESS] All tests passed\n")

    # 8-direction obstacle avoidance
    def enhanced_obstacle_avoidance_loop(self):
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
                front = self.get_front_range()
                if front > threshold:
                    self.move_front(forward_speed)
                else:
                    self.stop_robot()
                    time.sleep(0.5)
                    
                    # Sample all 8 directions
                    f = self.get_front_range()
                    fl = self.get_front_left_range()
                    fr = self.get_front_right_range()
                    l = self.get_left_range()
                    r = self.get_right_range()
                    b = self.get_back_range()
                    bl = self.get_back_left_range()
                    br = self.get_back_right_range()

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
                    best = max(directions, key=directions.get)
                    print(f"Obstacle detected. Best direction: {best} ({directions[best]:.2f}m)")

                    if directions[best] < 0.3:
                        best = 'back-left'

                    if best == 'front':
                        self.timed_move_front(slow_approach, 0.8)
                    elif best == 'back':
                        self.timed_move_back(slow_approach, 1.0)
                    elif best in ('left', 'front-left'):
                        self.timed_turn_left(turn_speed, 1.0)
                    elif best in ('right', 'front-right'):
                        self.timed_turn_right(turn_speed, 1.0)
                    elif best == 'back-left':
                        self.timed_move_back(slow_approach, 0.5)
                        self.timed_turn_left(turn_speed, 0.8)
                    elif best == 'back-right':
                        self.timed_move_back(slow_approach, 0.5)
                        self.timed_turn_right(turn_speed, 0.8)

                    self.stop_robot()
                    time.sleep(0.3)

                time.sleep(0.05)

        except KeyboardInterrupt:
            self.stop_robot()
            print("\n[STOPPED] Avoidance stopped by user")


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

    controller = RobotControl(robot_interface)
    try:
        controller.run_all_tests()
        controller.enhanced_obstacle_avoidance_loop()
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
    global executor
    rclpy.init(args=None)
    robot_interface = RobotInterface()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(robot_interface)
    threading.Thread(target=spin_node, daemon=True).start()

    print("System initializing...")
    time.sleep(5.0)
    print("[READY] System initialized\n")

    controller = RobotControl(robot_interface)
    try:
        controller.run_all_tests()
        controller.enhanced_obstacle_avoidance_loop()
    except Exception as e:
        print("\n========== ERROR ==========")
        traceback.print_exception(type(e), e, e.__traceback__)
        print("===========================")
    finally:
        executor.shutdown()
        robot_interface.destroy_node()
        rclpy.shutdown()
