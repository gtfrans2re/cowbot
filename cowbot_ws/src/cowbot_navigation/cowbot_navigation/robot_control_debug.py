#!/usr/bin/env python3

"""Debug version with detailed logging."""

import time
import math
import threading
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class RobotControlDebug(Node):
    def __init__(self):
        super().__init__('robot_control_debug')
        
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self._scan_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cowbot/cmd_vel', 10)
        
        self._scan_ranges = []
        self._scan_angle_min = 0.0
        self._scan_angle_max = 0.0
        self._scan_angle_increment = 0.0
        self._scan_lock = threading.Lock()
        
        self.get_logger().info('Robot Control Debug initialized')
    
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
    
    def _get_range_in_sector(self, center_angle: float, width: float) -> float:
        with self._scan_lock:
            if not self._scan_ranges:
                return float('inf')
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
            return float('inf')
        
        sector = ranges[start_idx:end_idx + 1]
        vals = [r for r in sector if not math.isinf(r) and not math.isnan(r)]
        
        # Debug: log sector info
        self.get_logger().debug(
            f"Sector center={center_angle:.2f}, width={width:.2f}: "
            f"indices {start_idx}-{end_idx}, {len(vals)}/{len(sector)} valid points"
        )
        
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
    
    def obstacle_avoidance_loop(self):
        print("\n=== Starting Obstacle Avoidance (Debug Mode) ===")
        print("Press Ctrl+C to stop\n")
        
        forward_speed = 0.2
        turn_speed = 0.5
        threshold = 0.4
        
        iteration = 0
        try:
            while rclpy.ok():
                iteration += 1
                
                # Get all ranges
                front = self.get_front_range()
                fl = self.get_front_left_range()
                fr = self.get_front_right_range()
                l = self.get_left_range()
                r = self.get_right_range()
                
                # Print detailed status every 20 iterations (~1 second)
                if iteration % 20 == 0:
                    print(f"\n--- Status (iteration {iteration}) ---")
                    print(f"Front:       {front:.2f}m {'[CLEAR]' if front > threshold else '[BLOCKED]'}")
                    print(f"Front-Left:  {fl:.2f}m")
                    print(f"Front-Right: {fr:.2f}m")
                    print(f"Left:        {l:.2f}m")
                    print(f"Right:       {r:.2f}m")
                    print(f"Threshold:   {threshold:.2f}m")
                
                if front > threshold:
                    # Clear path - move forward
                    self.move_front(forward_speed)
                    if iteration % 20 == 0:
                        print("→ ACTION: Moving forward")
                else:
                    # Obstacle detected
                    self.stop_robot()
                    print(f"\n!!! OBSTACLE DETECTED at {front:.2f}m !!!")
                    
                    directions = {
                        'front-left': fl,
                        'front-right': fr,
                        'left': l,
                        'right': r
                    }
                    
                    print("Clearances:")
                    for name, dist in directions.items():
                        print(f"  {name:12s}: {dist:.2f}m")
                    
                    best = max(directions, key=directions.get)
                    print(f"→ Best direction: {best} ({directions[best]:.2f}m)")
                    
                    # Turn towards best direction
                    if best in ('left', 'front-left'):
                        print("→ ACTION: Turning LEFT")
                        turn_count = 0
                        while self.get_front_range() <= threshold and rclpy.ok():
                            self.turn_left(turn_speed)
                            time.sleep(0.05)
                            turn_count += 1
                            if turn_count % 10 == 0:
                                print(f"  ... still turning (front now: {self.get_front_range():.2f}m)")
                    else:
                        print("→ ACTION: Turning RIGHT")
                        turn_count = 0
                        while self.get_front_range() <= threshold and rclpy.ok():
                            self.turn_right(turn_speed)
                            time.sleep(0.05)
                            turn_count += 1
                            if turn_count % 10 == 0:
                                print(f"  ... still turning (front now: {self.get_front_range():.2f}m)")
                    
                    self.stop_robot()
                    print(f"→ Turn complete. Front now: {self.get_front_range():.2f}m")
                    time.sleep(0.1)
                
                time.sleep(0.05)
        
        except KeyboardInterrupt:
            print("\n\n=== Stopped by user ===")
        finally:
            self.stop_robot()


def spin_in_thread(executor):
    try:
        executor.spin()
    except:
        pass


def main():
    rclpy.init()
    client = RobotControlDebug()
    
    executor = MultiThreadedExecutor()
    executor.add_node(client)
    spin_thread = threading.Thread(target=spin_in_thread, args=(executor,), daemon=True)
    spin_thread.start()
    
    print("Waiting for scan data...")
    time.sleep(2.0)
    
    try:
        client.obstacle_avoidance_loop()
    except KeyboardInterrupt:
        print("\n[STOPPED] Control stopped")
    finally:
        client.stop_robot()
        executor.shutdown()
        client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
