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

class RobotControl:
    def __init__(self, robot_interface: RobotInterface):
        self.robot_interface = robot_interface

    # ------------------------
    # Movement primitives
    # ------------------------
    def stop_robot(self):
        """Stop all motion."""
        self.robot_interface.linear_velocity = 0.0
        self.robot_interface.angular_velocity = 0.0

    def move_front(self, speed: float):
        """Drive straight forward."""
        self.robot_interface.linear_velocity = speed
        self.robot_interface.angular_velocity = 0.0

    def turn_left(self, speed: float):
        """Rotate in place left."""
        self.robot_interface.linear_velocity = 0.0
        self.robot_interface.angular_velocity = speed

    def turn_right(self, speed: float):
        """Rotate in place right."""
        self.robot_interface.linear_velocity = 0.0
        self.robot_interface.angular_velocity = -speed

    def timed_move_front(self, speed: float, duration: float):
        self.move_front(speed)
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

    # ------------------------
    # Laser‐Scanner accessors
    # ------------------------
    def _get_range_in_sector(self, center_angle: float, width: float) -> float:
        """
        Minimum range in [center_angle - width/2, center_angle + width/2].
        """
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

    # ------------------------
    # Test harness
    # ------------------------
    def run_all_tests(self):
        print("\n===== RUNNING ALL TESTS =====")
        self.stop_robot(); print("✓ stop_robot")
        self.move_front(0.2); time.sleep(0.5); self.stop_robot(); print("✓ move_front")
        self.turn_left(0.5); time.sleep(0.5); self.stop_robot(); print("✓ turn_left")
        self.turn_right(0.5); time.sleep(0.5); self.stop_robot(); print("✓ turn_right")
        self.timed_move_front(0.2, 1.0); print("✓ timed_move_front")
        self.timed_turn_left(0.5, 1.0); print("✓ timed_turn_left")
        self.timed_turn_right(0.5, 1.0); print("✓ timed_turn_right")
        self.move_distance_front(0.2, 0.2); print("✓ move_distance_front")
        self.turn_angle_left(0.5, 0.5); print("✓ turn_angle_left")
        print("Front-range sample:", self.get_front_range())
        print("\n✅ All tests passed!\n")

    # ------------------------
    # Enhanced obstacle avoidance
    # ------------------------
    def enhanced_obstacle_avoidance_loop(self):
        """
        Drive forward and avoid obstacles by picking the clearest of
        front-left, front-right, left, right sectors.
        """
        print("Starting enhanced avoidance loop. Ctrl+C to exit.")
        forward_speed = 0.2
        turn_speed    = 0.5
        threshold     = 0.4

        try:
            while True:
                front = self.get_front_range()
                if front > threshold:
                    self.move_front(forward_speed)
                else:
                    self.stop_robot()
                    fl = self.get_front_left_range()
                    fr = self.get_front_right_range()
                    l  = self.get_left_range()
                    r  = self.get_right_range()

                    directions = {
                        'front-left': fl,
                        'front-right': fr,
                        'left': l,
                        'right': r
                    }
                    best = max(directions, key=directions.get)
                    print(f"Obstacle! Best direction: {best} ({directions[best]:.2f}m)")

                    if best in ('left', 'front-left'):
                        while self.get_front_range() <= threshold:
                            self.turn_left(turn_speed)
                            time.sleep(0.05)
                    else:
                        while self.get_front_range() <= threshold:
                            self.turn_right(turn_speed)
                            time.sleep(0.05)

                    self.stop_robot()
                    time.sleep(0.1)

                time.sleep(0.05)

        except KeyboardInterrupt:
            self.stop_robot()
            print("\n🚧 Enhanced avoidance stopped by user.")


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

    controller = RobotControl(robot_interface)
    try:
        controller.run_all_tests()
        controller.enhanced_obstacle_avoidance_loop()
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
    global executor
    rclpy.init(args=None)
    robot_interface = RobotInterface()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(robot_interface)
    threading.Thread(target=spin_node, daemon=True).start()

    print("System ready in 5 seconds...")
    time.sleep(5.0)
    print("🚀 RUNNING\n")

    controller = RobotControl(robot_interface)
    try:
        controller.run_all_tests()
        controller.enhanced_obstacle_avoidance_loop()
    except Exception as e:
        print("~~~~~~~~~~~ ERROR ~~~~~~~~~~~")
        traceback.print_exception(type(e), e, e.__traceback__)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    finally:
        executor.shutdown()
        robot_interface.destroy_node()
        rclpy.shutdown()
