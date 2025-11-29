#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32MultiArray
import math
import threading


class RobotInterface(Node):
    """
    RobotInterface node that bridges LiDAR scan data, camera obstacle data,
    and cmd_vel commands with a parameter-based interface for easy scripting access.
    Implements sensor fusion between LiDAR and camera.
    """

    def __init__(self):
        super().__init__('robot_interface')
        
        # Declare parameters for cmd_vel control
        self.declare_parameter('cmd_vel_linear', 0.0)
        self.declare_parameter('cmd_vel_angular', 0.0)
        
        # Safety: motors only publish cmd_vel when enabled
        self.declare_parameter('motors_enabled', False)
        
        # Declare parameters for scan ranges (will be updated from scan topic)
        self.declare_parameter('scan_right_ray_range', float('inf'))
        self.declare_parameter('scan_front_right_ray_range', float('inf'))
        self.declare_parameter('scan_front_ray_range', float('inf'))
        self.declare_parameter('scan_front_left_ray_range', float('inf'))
        self.declare_parameter('scan_left_ray_range', float('inf'))
        
        # Declare parameters for fused sensor ranges
        self.declare_parameter('fused_right_range', float('inf'))
        self.declare_parameter('fused_front_right_range', float('inf'))
        self.declare_parameter('fused_front_range', float('inf'))
        self.declare_parameter('fused_front_left_range', float('inf'))
        self.declare_parameter('fused_left_range', float('inf'))
        
        # Declare parameters for sensor confidence/agreement
        self.declare_parameter('sensor_agreement_right', 1.0)
        self.declare_parameter('sensor_agreement_front_right', 1.0)
        self.declare_parameter('sensor_agreement_front', 1.0)
        self.declare_parameter('sensor_agreement_front_left', 1.0)
        self.declare_parameter('sensor_agreement_left', 1.0)
        
        # Declare parameters for odometry
        self.declare_parameter('odom_distance', 0.0)
        self.declare_parameter('odom_direction', 'N')
        self.declare_parameter('odom_position_x', 0.0)
        self.declare_parameter('odom_position_y', 0.0)
        self.declare_parameter('odom_position_z', 0.0)
        self.declare_parameter('odom_orientation_r', 0.0)
        self.declare_parameter('odom_orientation_p', 0.0)
        self.declare_parameter('odom_orientation_y', 0.0)
        
        # Declare parameters for IMU
        self.declare_parameter('imu_angular_velocity_x', 0.0)
        self.declare_parameter('imu_angular_velocity_y', 0.0)
        self.declare_parameter('imu_angular_velocity_z', 0.0)
        self.declare_parameter('imu_linear_acceleration_x', 0.0)
        self.declare_parameter('imu_linear_acceleration_y', 0.0)
        self.declare_parameter('imu_linear_acceleration_z', 0.0)
        
        # Internal state for scan data
        self._scan_ranges = []
        self._scan_angle_min = 0.0
        self._scan_angle_max = 0.0
        self._scan_angle_increment = 0.0
        self._scan_lock = threading.Lock()
        
        # Internal state for camera obstacle ranges
        # Sectors: [right, front_right, front, front_left, left]
        self._camera_ranges = [float('inf')] * 5
        self._camera_lock = threading.Lock()
        self._camera_available = False
        
        # Sensor fusion configuration
        self.lidar_weight = 0.6  # LiDAR more reliable for accurate distance
        self.camera_weight = 0.4  # Camera better for close-range and texture
        self.agreement_threshold = 0.2  # Range difference threshold for agreement (meters)
        
        # Internal state for odometry
        self._odom_x = 0.0
        self._odom_y = 0.0
        self._initial_x = None
        self._initial_y = None
        
        # Create subscribers
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self._scan_callback,
            10
        )
        
        self.camera_ranges_sub = self.create_subscription(
            Float32MultiArray,
            '/camera/obstacle_ranges',
            self._camera_ranges_callback,
            10
        )
        
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self._odom_callback,
            10
        )
        
        self.imu_sub = self.create_subscription(
            Imu,
            '/imu',
            self._imu_callback,
            10
        )
        
        # Create publisher for cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, '/cowbot/cmd_vel', 10)
        
        # Create timer to publish cmd_vel based on parameters
        self.timer = self.create_timer(0.1, self._timer_callback)
        
        self.get_logger().info('RobotInterface node initialized with sensor fusion')
    
    def _scan_callback(self, msg: LaserScan):
        """Process incoming laser scan data and update parameters."""
        with self._scan_lock:
            self._scan_ranges = list(msg.ranges)
            self._scan_angle_min = msg.angle_min
            self._scan_angle_max = msg.angle_max
            self._scan_angle_increment = msg.angle_increment
        
        # Update scan range parameters for different sectors
        try:
            right = self._get_min_range_in_sector(-math.pi/2, math.pi/6)
            front_right = self._get_min_range_in_sector(-math.pi/4, math.pi/6)
            front = self._get_min_range_in_sector(0.0, math.pi/6)
            front_left = self._get_min_range_in_sector(math.pi/4, math.pi/6)
            left = self._get_min_range_in_sector(math.pi/2, math.pi/6)
            
            self.set_parameters([
                Parameter('scan_right_ray_range', Parameter.Type.DOUBLE, right),
                Parameter('scan_front_right_ray_range', Parameter.Type.DOUBLE, front_right),
                Parameter('scan_front_ray_range', Parameter.Type.DOUBLE, front),
                Parameter('scan_front_left_ray_range', Parameter.Type.DOUBLE, front_left),
                Parameter('scan_left_ray_range', Parameter.Type.DOUBLE, left),
            ])
            
            # Perform sensor fusion
            self._fuse_sensors()
            
        except Exception as e:
            self.get_logger().warn(f'Error updating scan parameters: {e}')
    
    def _camera_ranges_callback(self, msg: Float32MultiArray):
        """Process incoming camera obstacle ranges."""
        with self._camera_lock:
            if len(msg.data) >= 5:
                self._camera_ranges = list(msg.data[:5])
                self._camera_available = True
                
                # Perform sensor fusion
                self._fuse_sensors()
    
    def _fuse_sensors(self):
        """
        Fuse LiDAR and camera sensor data.
        Uses conservative approach: minimum range from either sensor.
        Calculates sensor agreement score for decision making.
        """
        lidar_ranges = [
            self.get_parameter('scan_right_ray_range').value,
            self.get_parameter('scan_front_right_ray_range').value,
            self.get_parameter('scan_front_ray_range').value,
            self.get_parameter('scan_front_left_ray_range').value,
            self.get_parameter('scan_left_ray_range').value,
        ]
        
        with self._camera_lock:
            camera_ranges = self._camera_ranges.copy()
            camera_available = self._camera_available
        
        fused_ranges = []
        agreement_scores = []
        
        for i in range(5):
            lidar_range = lidar_ranges[i]
            camera_range = camera_ranges[i] if camera_available else float('inf')
            
            # Conservative fusion: use minimum range
            if math.isinf(lidar_range) and math.isinf(camera_range):
                fused_range = float('inf')
            elif math.isinf(lidar_range):
                fused_range = camera_range
            elif math.isinf(camera_range):
                fused_range = lidar_range
            else:
                # Both sensors have valid readings
                # Use weighted average if close, minimum if disagreement
                range_diff = abs(lidar_range - camera_range)
                
                if range_diff < self.agreement_threshold:
                    # Sensors agree - weighted average
                    fused_range = (self.lidar_weight * lidar_range + 
                                 self.camera_weight * camera_range)
                else:
                    # Sensors disagree - use minimum (conservative)
                    fused_range = min(lidar_range, camera_range)
            
            fused_ranges.append(fused_range)
            
            # Calculate agreement score (1.0 = full agreement, 0.0 = strong disagreement)
            if math.isinf(lidar_range) or math.isinf(camera_range):
                agreement = 0.5  # Partial confidence with only one sensor
            else:
                range_diff = abs(lidar_range - camera_range)
                # Normalize to 0-1 scale (0.5m difference = 0 agreement)
                agreement = max(0.0, 1.0 - (range_diff / 0.5))
            
            agreement_scores.append(agreement)
        
        # Update fused parameters
        param_names = [
            'fused_right_range',
            'fused_front_right_range',
            'fused_front_range',
            'fused_front_left_range',
            'fused_left_range',
        ]
        
        agreement_names = [
            'sensor_agreement_right',
            'sensor_agreement_front_right',
            'sensor_agreement_front',
            'sensor_agreement_front_left',
            'sensor_agreement_left',
        ]
        
        params = []
        for i in range(5):
            params.append(Parameter(param_names[i], Parameter.Type.DOUBLE, fused_ranges[i]))
            params.append(Parameter(agreement_names[i], Parameter.Type.DOUBLE, agreement_scores[i]))
        
        self.set_parameters(params)
    
    def _get_min_range_in_sector(self, center_angle: float, width: float) -> float:
        """Get minimum range in a sector defined by center angle and width."""
        with self._scan_lock:
            if not self._scan_ranges:
                return float('inf')
            
            start_angle = center_angle - width / 2
            end_angle = center_angle + width / 2
            
            start_idx = int((start_angle - self._scan_angle_min) / self._scan_angle_increment)
            end_idx = int((end_angle - self._scan_angle_min) / self._scan_angle_increment)
            
            start_idx = max(0, start_idx)
            end_idx = min(len(self._scan_ranges) - 1, end_idx)
            
            if start_idx >= len(self._scan_ranges) or end_idx < 0:
                return float('inf')
            
            sector = self._scan_ranges[start_idx:end_idx + 1]
            valid_ranges = [r for r in sector if not math.isinf(r) and not math.isnan(r)]
            
            return min(valid_ranges) if valid_ranges else float('inf')
    
    def _odom_callback(self, msg: Odometry):
        """Process odometry data and update parameters."""
        # Update position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        
        # Initialize starting position
        if self._initial_x is None:
            self._initial_x = x
            self._initial_y = y
        
        # Calculate distance traveled
        dx = x - self._initial_x
        dy = y - self._initial_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Calculate orientation (yaw)
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        
        # Convert quaternion to Euler angles
        roll, pitch, yaw = self._quaternion_to_euler(qx, qy, qz, qw)
        
        # Determine cardinal direction
        direction = self._yaw_to_direction(yaw)
        
        self.set_parameters([
            Parameter('odom_distance', Parameter.Type.DOUBLE, distance),
            Parameter('odom_direction', Parameter.Type.STRING, direction),
            Parameter('odom_position_x', Parameter.Type.DOUBLE, x),
            Parameter('odom_position_y', Parameter.Type.DOUBLE, y),
            Parameter('odom_position_z', Parameter.Type.DOUBLE, z),
            Parameter('odom_orientation_r', Parameter.Type.DOUBLE, roll),
            Parameter('odom_orientation_p', Parameter.Type.DOUBLE, pitch),
            Parameter('odom_orientation_y', Parameter.Type.DOUBLE, yaw),
        ])
    
    def _imu_callback(self, msg: Imu):
        """Process IMU data and update parameters."""
        self.set_parameters([
            Parameter('imu_angular_velocity_x', Parameter.Type.DOUBLE, msg.angular_velocity.x),
            Parameter('imu_angular_velocity_y', Parameter.Type.DOUBLE, msg.angular_velocity.y),
            Parameter('imu_angular_velocity_z', Parameter.Type.DOUBLE, msg.angular_velocity.z),
            Parameter('imu_linear_acceleration_x', Parameter.Type.DOUBLE, msg.linear_acceleration.x),
            Parameter('imu_linear_acceleration_y', Parameter.Type.DOUBLE, msg.linear_acceleration.y),
            Parameter('imu_linear_acceleration_z', Parameter.Type.DOUBLE, msg.linear_acceleration.z),
        ])
    
    def _quaternion_to_euler(self, x, y, z, w):
        """Convert quaternion to roll, pitch, yaw."""
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)
        
        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)
        
        # Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        return roll, pitch, yaw
    
    def _yaw_to_direction(self, yaw):
        """Convert yaw angle to cardinal direction."""
        # Normalize yaw to [0, 2*pi]
        yaw = yaw % (2 * math.pi)
        
        # Convert to degrees
        degrees = math.degrees(yaw)
        
        # Determine direction
        if degrees < 22.5 or degrees >= 337.5:
            return 'E'
        elif degrees < 67.5:
            return 'NE'
        elif degrees < 112.5:
            return 'N'
        elif degrees < 157.5:
            return 'NW'
        elif degrees < 202.5:
            return 'W'
        elif degrees < 247.5:
            return 'SW'
        elif degrees < 292.5:
            return 'S'
        else:
            return 'SE'
    
    def _timer_callback(self):
        """Publish cmd_vel based on parameters."""
        # Safety gate: only publish if motors enabled
        if not self.get_parameter('motors_enabled').value:
            return
        
        linear = self.get_parameter('cmd_vel_linear').value
        angular = self.get_parameter('cmd_vel_angular').value
        
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        
        self.cmd_vel_pub.publish(twist)
    
    # Properties for direct Python access
    @property
    def linear_velocity(self):
        return self.get_parameter('cmd_vel_linear').value
    
    @linear_velocity.setter
    def linear_velocity(self, value):
        self.set_parameters([Parameter('cmd_vel_linear', Parameter.Type.DOUBLE, float(value))])
    
    @property
    def angular_velocity(self):
        return self.get_parameter('cmd_vel_angular').value
    
    @angular_velocity.setter
    def angular_velocity(self, value):
        self.set_parameters([Parameter('cmd_vel_angular', Parameter.Type.DOUBLE, float(value))])
    
    @property
    def motors_enabled(self):
        return self.get_parameter('motors_enabled').value
    
    @motors_enabled.setter
    def motors_enabled(self, value: bool):
        self.set_parameters([Parameter('motors_enabled', Parameter.Type.BOOL, bool(value))])
    
    @property
    def scan_ranges(self):
        with self._scan_lock:
            return self._scan_ranges.copy()
    
    @property
    def scan_angle_min(self):
        return self._scan_angle_min
    
    @property
    def scan_angle_max(self):
        return self._scan_angle_max
    
    @property
    def scan_angle_increment(self):
        return self._scan_angle_increment


def main(args=None):
    if not rclpy.ok():
        rclpy.init(args=args)
    robot_interface = RobotInterface()
    
    try:
        rclpy.spin(robot_interface)
    except KeyboardInterrupt:
        pass
    finally:
        robot_interface.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
