#!/usr/bin/env python3
"""
Camera-based obstacle detection node for cowbot.
Processes camera images to detect obstacles and estimate distances.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
import cv2
from cv_bridge import CvBridge
import numpy as np
import math


class CameraObstacleDetector(Node):
    """
    Detects obstacles using camera image processing and estimates their distances.
    Divides the field of view into sectors matching LiDAR configuration.
    """

    def __init__(self):
        super().__init__('camera_obstacle_detector')
        
        # Camera parameters
        self.image_width = 800
        self.image_height = 800
        self.horizontal_fov = 1.3962634  # ~80 degrees in radians
        
        # Detection parameters
        self.min_contour_area = 500  # Minimum contour area to consider as obstacle
        self.max_detection_range = 2.0  # Maximum reliable detection range in meters
        self.min_detection_range = 0.1  # Minimum detection range in meters
        
        # Calibration constant for distance estimation (will need tuning)
        # Assumes obstacle average height of ~0.3m at 1m distance occupies certain pixels
        self.distance_calibration = 15000.0
        
        # Define sectors matching LiDAR angular divisions
        # Sectors: [right, front_right, front, front_left, left]
        # Angles relative to forward (0 = forward, positive = left, negative = right)
        self.sector_angles = [
            -math.pi/2,      # right: -90 degrees
            -math.pi/4,      # front_right: -45 degrees
            0.0,             # front: 0 degrees
            math.pi/4,       # front_left: 45 degrees
            math.pi/2        # left: 90 degrees
        ]
        self.sector_width = math.pi/3  # 60 degrees per sector
        
        # Initialize ranges for each sector (set to max initially)
        self.camera_ranges = [self.max_detection_range] * 5
        
        # CV Bridge for ROS-OpenCV conversion
        self.bridge = CvBridge()
        
        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        # Publisher for camera-detected ranges
        self.ranges_pub = self.create_publisher(
            Float32MultiArray,
            '/camera/obstacle_ranges',
            10
        )
        
        self.get_logger().info('Camera obstacle detector initialized')

    def image_callback(self, msg):
        """Process incoming camera image and detect obstacles."""
        try:
            # Convert ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            
            
            # Convert YUYV to BGR if needed
            if msg.encoding == "yuyv" or msg.encoding == "yuv422_yuy2":
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_YUV2BGR_YUY2)
            elif len(cv_image.shape) == 2 or cv_image.shape[2] == 1:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
            # Process image to detect obstacles
            obstacle_detections = self.detect_obstacles(cv_image)
            
            # Convert detections to sector-based ranges
            self.camera_ranges = self.compute_sector_ranges(obstacle_detections)
            
            # Publish ranges
            ranges_msg = Float32MultiArray()
            ranges_msg.data = self.camera_ranges
            self.ranges_pub.publish(ranges_msg)
            
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

    def detect_obstacles(self, image):
        """
        Detect obstacles in the image using edge detection and contour analysis.
        
        Returns:
            List of tuples: [(angle, distance), ...] for each detected obstacle
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection using Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        # Morphological operations to connect edges
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=2)
        closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter small contours
            if area < self.min_contour_area:
                continue
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calculate centroid
            M = cv2.moments(contour)
            if M['m00'] == 0:
                continue
            
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            
            # Estimate angle based on horizontal position
            # Center of image is 0 degrees (forward)
            # Left side is positive, right side is negative
            pixel_offset = cx - (self.image_width / 2)
            angle = (pixel_offset / self.image_width) * self.horizontal_fov
            
            # Estimate distance based on obstacle size and vertical position
            # Objects lower in the frame are closer
            # Objects that appear larger are closer
            distance = self.estimate_distance(w, h, cy, area)
            
            detections.append((angle, distance))
        
        return detections

    def estimate_distance(self, width, height, center_y, area):
        """
        Estimate distance to obstacle based on its appearance in the image.
        
        Args:
            width: Width of bounding box in pixels
            height: Height of bounding box in pixels
            center_y: Vertical center position in image
            area: Contour area in pixels
            
        Returns:
            Estimated distance in meters
        """
        # Method 1: Use area (larger area = closer)
        # Assuming inverse square relationship
        if area > 0:
            distance_from_area = math.sqrt(self.distance_calibration / area)
        else:
            distance_from_area = self.max_detection_range
        
        # Method 2: Use vertical position (lower in frame = closer)
        # Objects at bottom of frame are closest
        vertical_ratio = center_y / self.image_height
        # Map vertical position: bottom (1.0) -> min_range, middle (0.5) -> mid_range
        distance_from_position = self.min_detection_range + (1.0 - vertical_ratio) * self.max_detection_range
        
        # Combine both methods with weighting (area is more reliable)
        distance = 0.7 * distance_from_area + 0.3 * distance_from_position
        
        # Clamp to valid range
        distance = max(self.min_detection_range, min(self.max_detection_range, distance))
        
        return distance

    def compute_sector_ranges(self, detections):
        """
        Convert obstacle detections to minimum range per sector.
        
        Args:
            detections: List of (angle, distance) tuples
            
        Returns:
            List of 5 range values, one per sector
        """
        # Initialize all sectors to max range
        sector_ranges = [self.max_detection_range] * 5
        
        # Assign each detection to appropriate sector(s)
        for angle, distance in detections:
            for i, sector_angle in enumerate(self.sector_angles):
                # Check if detection falls within this sector
                angle_diff = abs(angle - sector_angle)
                
                if angle_diff <= self.sector_width / 2:
                    # Update sector with minimum distance
                    sector_ranges[i] = min(sector_ranges[i], distance)
        
        return sector_ranges


def main(args=None):
    rclpy.init(args=args)
    detector = CameraObstacleDetector()
    
    try:
        rclpy.spin(detector)
    except KeyboardInterrupt:
        pass
    finally:
        detector.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
