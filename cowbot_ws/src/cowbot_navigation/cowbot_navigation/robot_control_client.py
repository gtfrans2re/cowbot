#!/usr/bin/env python3

"""Robot control client with slow and deliberate obstacle avoidance."""

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
    # Laser-Scanner accessors
    # ------------------------
    def _get_range_in_sector(self, center_angle: float, width: float) -> float:
        """
        Minimum range in [center_angle - width/2, center_angle + width/2].
        """
        angles = self.robot_interface.scan_ranges
        amin = self.robot_interface.scan_angle_min
        inc = self.robot_interface.scan_angle_increment
        
        # Guard against uninitialized scan data
        if inc == 0.0 or len(angles) == 0:
            return float('inf')
        
        n = len(angles)
        start = int((center_angle - width/2 - amin) / inc)
        end = int((center_angle + width/2 - amin) / inc)
        start = max(0, start)
        end = min(n-1, end)
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
        # SAFETY: Now enable motors for autonomous operation
        self.robot_interface.motors_enabled = True
        print("🔓 Motors ENABLED for autonomous operation\n")

    # ------------------------
    # SLOW & DELIBERATE obstacle avoidance
    # ------------------------
    def enhanced_obstacle_avoidance_loop(self):
        """
        Slow and deliberate navigation:
        - Moves slowly forward when path is clear
        - STOPS completely when obstacle detected
        - Pauses to assess all directions
        - Turns slowly toward best clearance
        - No backward movement
        """
        print("Starting SLOW & DELIBERATE avoidance loop. Ctrl+C to exit.")
        
        # Adaptive speeds - slower near obstacles, faster in open space
        min_forward_speed = 0.010   # Very slow near obstacles
        max_forward_speed = 0.025   # Faster in open areas
        min_turn_speed = 0.06       # Slow turns
        max_turn_speed = 0.12       # Faster turns
        threshold = 0.6             # Start slowing down distance
        danger_threshold = 0.4      # Critical distance - stop/turn

        try:
            while True:
                front = self.get_front_range()
                
                if front > threshold:
                    # Path is clear - move forward slowly
                    # Use slow fallback speed when adaptive not calculated
                    fallback_speed = min_forward_speed
                    self.move_front(fallback_speed)
                    print(f"✓ Moving forward slowly: front={front:.2f}m")
                    time.sleep(0.2)  # Slower loop cycle
                else:
                    # OBSTACLE DETECTED - STOP IMMEDIATELY
                    self.stop_robot()
                    print(f"\n⚠️  OBSTACLE at {front:.2f}m - STOPPED")
                    
                    # PAUSE to stabilize (important!)
                    time.sleep(0.5)
                    
                    # Sample ALL directions after stopping
                    fl = self.get_front_left_range()
                    fr = self.get_front_right_range()
                    l = self.get_left_range()
                    r = self.get_right_range()
                    
                    # Display what robot sees
                    print(f"📊 Scan: F={front:.2f}m  FL={fl:.2f}m  FR={fr:.2f}m  L={l:.2f}m  R={r:.2f}m")
                    
                    # Find best clearance (exclude backward, only forward-facing directions)
                    directions = {
                        'front-left': fl,
                        'front-right': fr,
                        'left': l,
                        'right': r
                    }
                    best = max(directions, key=directions.get)
                    best_clearance = directions[best]
                    
                    print(f"🎯 Best direction: {best} ({best_clearance:.2f}m clearance)")
                    
                    # If all blocked, default to left
                    if best_clearance < 0.3:
                        print("⚠️  All directions tight, defaulting to LEFT")
                        best = 'left'
                    
                    # TURN SLOWLY toward best direction
                    if best in ('left', 'front-left'):
                        # Adaptive turn: faster when more clearance
                        clearance = best_clearance
                        turn_ratio = min(clearance / 1.0, 1.0)  # 1m clearance = full speed
                        adaptive_turn = min_turn_speed + (max_turn_speed - min_turn_speed) * turn_ratio
                        print(f"↺ Turning LEFT (speed={adaptive_turn:.2f}rad/s, clearance={clearance:.2f}m)...")
                        self.timed_turn_left(adaptive_turn, 1.2)  # Shorter turn time
                        time.sleep(0.3)  # Pause after turn
                    elif best in ('right', 'front-right'):
                        clearance = best_clearance
                        turn_ratio = min(clearance / 1.0, 1.0)
                        adaptive_turn = min_turn_speed + (max_turn_speed - min_turn_speed) * turn_ratio
                        print(f"↻ Turning RIGHT (speed={adaptive_turn:.2f}rad/s, clearance={clearance:.2f}m)...")
                        self.timed_turn_right(adaptive_turn, 1.2)
                        time.sleep(0.3)  # Pause after turn
                    
                    self.stop_robot()
                    print("✓ Turn complete, reassessing...\n")
                    time.sleep(0.3)  # Additional pause before moving again
                
                time.sleep(0.05)  # Responsive main loop (was 0.1)

        except KeyboardInterrupt:
            try:
                self.stop_robot()
            except Exception:
                pass  # Context may already be shutdown
            print("\n🚧 Avoidance stopped by user.")


def main():
    if not rclpy.ok():
        rclpy.init(args=None)
    robot_interface = RobotInterface()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(robot_interface)
    
    # Start executor in a separate thread
    def spin_node():
        executor.spin()
    
    spin_thread = threading.Thread(target=spin_node, daemon=True)
    spin_thread.start()

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
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
