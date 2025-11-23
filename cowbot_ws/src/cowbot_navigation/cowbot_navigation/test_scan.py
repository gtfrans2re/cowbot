#!/usr/bin/env python3
"""Quick test to see what scan data looks like."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class ScanTest(Node):
    def __init__(self):
        super().__init__('scan_test')
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.count = 0
    
    def scan_callback(self, msg):
        self.count += 1
        if self.count % 10 == 0:  # Every 10th message
            ranges = list(msg.ranges)
            valid_ranges = [r for r in ranges if not math.isinf(r) and not math.isnan(r)]
            
            self.get_logger().info(
                f"Scan: {len(ranges)} points, {len(valid_ranges)} valid, "
                f"angle_min={msg.angle_min:.2f}, angle_max={msg.angle_max:.2f}, "
                f"angle_increment={msg.angle_increment:.4f}"
            )
            if valid_ranges:
                self.get_logger().info(
                    f"  Range: min={min(valid_ranges):.2f}m, max={max(valid_ranges):.2f}m, "
                    f"avg={sum(valid_ranges)/len(valid_ranges):.2f}m"
                )
            else:
                self.get_logger().warn("  NO VALID RANGES!")

def main():
    rclpy.init()
    node = ScanTest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
