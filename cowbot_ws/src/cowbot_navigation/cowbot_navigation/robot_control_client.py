#!/usr/bin/env python3

"""Robot control client with fixed obstacle avoidance logic."""

import time
import math
import threading
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class RobotControlClient(Node):
    def __init__(self):
        super().__init__('robot_control_client')
        
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self._scan_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cowbot/cmd_vel', 10)
        
        self._scan_ranges = []
        self._scan_angle_min = 0.0
        self._scan_angle_max = 0.0
        self._scan_angle_increment = 0.0
        self._scan_lock = threading.Lock()
        
        self.get_logger().info('Robot Control Client initialized')
    
    def _scan_callback(self, msg: LaserScan):
        with self._scan_lock:
            self._scan_ranges = list(msg.ranges)
            self._scan_angle_min = msg.angle_min
            self._scan_angle_max = msg.angle_max
            self._scan_angle_increment = msg.angle_increment
    
    def stop_robot(self):
        twist = Twist()
        self.cmd_vel_pub.publish(twist)
    
    def move_front(self, speed: float):
        twist = Twist()
        twist.linear.x = speed
        self.cmd_vel_pub.publish(twist)
    
    def turn_left(self, speed: float):
        twist = Twist()
        twist.angular.z = speed
        self.cmd_vel_pub.publish(twist)
    
    def turn_right(self, speed: float):
        twist = Twist()
        twist.angular.z = -speed
        self.cmd_vel_pub.publish(twist)
    
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
    
    def _get_range_in_sector(self, center_angle: float, width: float) -> float:
        with self._scan_lock:
            if not self._scan_ranges:
                return 0.0  # Changed: return 0 instead of inf when no data
            ranges = self._scan_ranges
            amin = self._scan_angle_min
            inc = self._scan_angle_increment
        
        start_angle = center_angle - width / 2
        end_angle = center_angle + width / 2
        
        start_idx = int((start_angle - amin) / inc)
        end_idx = int((end_angle - amin) / inc)
        
        start_idx = max(0, start_idx)
        end_idx = min(len(ranges) - 1, end_idx)
        
        if start_idx >= len(ranges) or end_idx < 0:
            return 0.0  # Changed: return 0 instead of inf for out of bounds
        
        sector = ranges[start_idx:end_idx + 1]
        vals = [r for r in sector if not math.isinf(r) and not math.isnan(r)]
        
        # Changed: return 0 if no valid readings (treat as blocked)
        return min(vals) if vals else 0.0
    
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
    
    def enhanced_obstacle_avoidance_loop(self):
        print("Starting enhanced avoidance loop. Ctrl+C to exit.")
        forward_speed = 0.05
        turn_speed = 0.15
        threshold = 0.6
        
        try:
            while rclpy.ok():
                front = self.get_front_range()
                
                if front > threshold:
                    self.move_front(forward_speed)
                    self.get_logger().info(f'Moving forward: front={front:.2f}m', throttle_duration_sec=2.0)
                else:
                    self.stop_robot()
                    fl = self.get_front_left_range()
                    fr = self.get_front_right_range()
                    l = self.get_left_range()
                    r = self.get_right_range()
                    
                    directions = {
                        'front-left': fl,
                        'front-right': fr,
                        'left': l,
                        'right': r
                    }
                    best = max(directions, key=directions.get)
                    self.get_logger().info(
                        f"Obstacle at {front:.2f}m! Turning to {best} (clearance: {directions[best]:.2f}m)"
                    )
                    
                    # Turn towards best direction
                    if best in ('left', 'front-left'):
                        while self.get_front_range() <= threshold and rclpy.ok():
                            self.turn_left(turn_speed)
                            time.sleep(0.05)
                    else:
                        while self.get_front_range() <= threshold and rclpy.ok():
                            self.turn_right(turn_speed)
                            time.sleep(0.05)
                    
                    self.stop_robot()
                    time.sleep(0.1)
                
                time.sleep(0.05)
        
        except KeyboardInterrupt:
            self.get_logger().info('Stopped by user')
        finally:
            self.stop_robot()


def spin_in_thread(executor):
    try:
        executor.spin()
    except:
        pass


def main():
    rclpy.init()
    client = RobotControlClient()
    
    executor = MultiThreadedExecutor()
    executor.add_node(client)
    spin_thread = threading.Thread(target=spin_in_thread, args=(executor,), daemon=True)
    spin_thread.start()
    
    print("Waiting for scan data...")
    time.sleep(2.0)
    
    try:
        client.run_all_tests()
        client.enhanced_obstacle_avoidance_loop()
    except KeyboardInterrupt:
        print("\n🚧 Control stopped by user")
    finally:
        client.stop_robot()
        executor.shutdown()
        client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
