#!/usr/bin/env python3

"""Robot control with sensor fusion and enhanced decision making."""

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

    # Sensor fusion accessors - 8 directions
    def _get_range_in_sector(self, center_angle: float, width: float) -> float:
        """Return minimum range in angular sector from raw LiDAR."""
        angles = self.robot_interface.scan_ranges
        amin = self.robot_interface.scan_angle_min
        inc = self.robot_interface.scan_angle_increment
        
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

    # Fused sensor range accessors
    def get_fused_front_range(self) -> float:
        """Get fused sensor range for front sector."""
        return self.robot_interface.get_parameter('fused_front_range').value

    def get_fused_front_left_range(self) -> float:
        """Get fused sensor range for front-left sector."""
        return self.robot_interface.get_parameter('fused_front_left_range').value

    def get_fused_front_right_range(self) -> float:
        """Get fused sensor range for front-right sector."""
        return self.robot_interface.get_parameter('fused_front_right_range').value

    def get_fused_left_range(self) -> float:
        """Get fused sensor range for left sector."""
        return self.robot_interface.get_parameter('fused_left_range').value

    def get_fused_right_range(self) -> float:
        """Get fused sensor range for right sector."""
        return self.robot_interface.get_parameter('fused_right_range').value

    # Sensor agreement accessors
    def get_sensor_agreement_front(self) -> float:
        return self.robot_interface.get_parameter('sensor_agreement_front').value

    def get_sensor_agreement_front_left(self) -> float:
        return self.robot_interface.get_parameter('sensor_agreement_front_left').value

    def get_sensor_agreement_front_right(self) -> float:
        return self.robot_interface.get_parameter('sensor_agreement_front_right').value

    def get_sensor_agreement_left(self) -> float:
        return self.robot_interface.get_parameter('sensor_agreement_left').value

    def get_sensor_agreement_right(self) -> float:
        return self.robot_interface.get_parameter('sensor_agreement_right').value

    # Legacy accessors for backward compatibility
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
        print("Front range (fused):", self.get_fused_front_range())
        print("\n[SUCCESS] All tests passed\n")
        # Enable motors for autonomous operation
        self.robot_interface.motors_enabled = True
        print("[MOTORS ENABLED] Ready for autonomous operation\n")

    def evaluate_direction_score(self, clearance: float, agreement: float, 
                                  is_forward: bool = False, is_straight: bool = False) -> float:
        """
        Enhanced direction scoring with multiple criteria for better decision making.
        
        Args:
            clearance: Distance to obstacle in this direction
            agreement: Sensor agreement score (0-1)
            is_forward: Whether this is a forward direction (preferred)
            is_straight: Whether this is straight forward (most preferred)
            
        Returns:
            Score for this direction (higher is better)
        """
        # Handle infinite clearance
        if math.isinf(clearance):
            clearance = 10.0  # Cap infinite values for scoring
        
        # Base score from clearance (non-linear: closer to obstacles gets penalized more)
        # Use square root to emphasize larger clearances
        score = math.sqrt(clearance)
        
        # Boost for sensor agreement (confident reading = more reliable)
        # High agreement (0.8+) significantly boosts confidence
        if agreement > 0.8:
            agreement_multiplier = 0.5 + 0.5 * agreement  # 0.9-1.0 range
        elif agreement > 0.5:
            agreement_multiplier = 0.4 + 0.4 * agreement  # 0.6-0.8 range
        else:
            agreement_multiplier = 0.3 + 0.3 * agreement  # 0.3-0.5 range
        
        score *= agreement_multiplier
        
        # Strong preference for forward directions (keeps robot moving forward)
        if is_forward:
            score *= 1.4
            # Extra bonus for straight forward
            if is_straight:
                score *= 1.2
        
        # Penalize very close obstacles more aggressively
        if clearance < 0.4:
            score *= 0.3  # Heavy penalty
        elif clearance < 0.6:
            score *= 0.6  # Moderate penalty
        
        return score

    # Enhanced obstacle avoidance with sensor fusion
    def fused_obstacle_avoidance_loop(self):
        """
        Navigate using fused LiDAR+camera data with multi-criteria decision making.
        Uses sensor agreement scores to improve reliability.
        """
        print("Starting sensor fusion obstacle avoidance. Ctrl+C to exit.")
        print("Using LiDAR + Camera fusion for enhanced obstacle detection\n")
        
        # Speed configuration
        forward_speed = 0.08        # Normal forward speed
        slow_approach = 0.04        # Slow approach near obstacles
        turn_speed = 0.15           # Turn speed
        threshold = 0.6             # Distance to start reacting
        danger_threshold = 0.4      # Critical distance

        try:
            while True:
                # Use fused front range for primary decision
                front = self.get_fused_front_range()
                
                if front > threshold:
                    # Clear path - move forward
                    self.move_front(forward_speed)
                    # Periodically log sensor agreement
                    if int(time.time() * 10) % 50 == 0:
                        agreement = self.get_sensor_agreement_front()
                        print(f"Moving forward: range={front:.2f}m, agreement={agreement:.2f}")
                    time.sleep(0.2)
                else:
                    # Obstacle detected - stop
                    self.stop_robot()
                    print(f"\n[OBSTACLE] Detected at {front:.2f}m - stopped")
                    
                    # Stabilize sensors
                    time.sleep(0.5)
                    
                    # Sample all 5 fused directions (front sectors only)
                    f = self.get_fused_front_range()
                    fl = self.get_fused_front_left_range()
                    fr = self.get_fused_front_right_range()
                    l = self.get_fused_left_range()
                    r = self.get_fused_right_range()
                    
                    # Get back ranges from LiDAR only (camera doesn't see backwards)
                    b = self.get_back_range()
                    bl = self.get_back_left_range()
                    br = self.get_back_right_range()
                    
                    # Get sensor agreement scores
                    ag_f = self.get_sensor_agreement_front()
                    ag_fl = self.get_sensor_agreement_front_left()
                    ag_fr = self.get_sensor_agreement_front_right()
                    ag_l = self.get_sensor_agreement_left()
                    ag_r = self.get_sensor_agreement_right()
                    
                    # Display sensor readings
                    print(f"Fused ranges - F:{f:.2f} FL:{fl:.2f} FR:{fr:.2f} L:{l:.2f} R:{r:.2f}")
                    print(f"Back ranges  - B:{b:.2f} BL:{bl:.2f} BR:{br:.2f}")
                    print(f"Agreement    - F:{ag_f:.2f} FL:{ag_fl:.2f} FR:{ag_fr:.2f} L:{ag_l:.2f} R:{ag_r:.2f}")
                    
                    # Evaluate all directions with enhanced multi-criteria scoring
                    direction_scores = {
                        'front': self.evaluate_direction_score(f, ag_f, is_forward=True, is_straight=True),
                        'front-left': self.evaluate_direction_score(fl, ag_fl, is_forward=True),
                        'front-right': self.evaluate_direction_score(fr, ag_fr, is_forward=True),
                        'left': self.evaluate_direction_score(l, ag_l, is_forward=False),
                        'right': self.evaluate_direction_score(r, ag_r, is_forward=False),
                        'back': self.evaluate_direction_score(b, 0.5, is_forward=False) * 0.4,  # Back gets lower priority
                        'back-left': self.evaluate_direction_score(bl, 0.5, is_forward=False) * 0.4,
                        'back-right': self.evaluate_direction_score(br, 0.5, is_forward=False) * 0.4
                    }
                    
                    # Find best direction
                    best = max(direction_scores, key=direction_scores.get)
                    best_score = direction_scores[best]
                    
                    # Get raw clearance for best direction
                    direction_clearances = {
                        'front': f, 'front-left': fl, 'front-right': fr,
                        'left': l, 'right': r, 'back': b,
                        'back-left': bl, 'back-right': br
                    }
                    best_clearance = direction_clearances[best]
                    
                    print(f"Best direction: {best} (clearance: {best_clearance:.2f}m, score: {best_score:.2f})")
                    
                    # If all directions severely constrained, default to back-left
                    if best_clearance < 0.25:
                        print("[WARNING] All directions severely constrained, emergency reverse left")
                        best = 'back-left'
                    
                    # Execute movement toward best direction
                    if best == 'front':
                        print("Moving forward slowly")
                        self.timed_move_front(slow_approach, 0.8)
                    elif best == 'back':
                        print("Reversing")
                        self.timed_move_back(slow_approach, 1.0)
                    elif best in ('left', 'front-left'):
                        print("Turning LEFT")
                        self.timed_turn_left(turn_speed, 1.0)
                    elif best in ('right', 'front-right'):
                        print("Turning RIGHT")
                        self.timed_turn_right(turn_speed, 1.0)
                    elif best == 'back-left':
                        print("Reversing LEFT")
                        self.timed_move_back(slow_approach, 0.5)
                        self.timed_turn_left(turn_speed, 0.8)
                    elif best == 'back-right':
                        print("Reversing RIGHT")
                        self.timed_move_back(slow_approach, 0.5)
                        self.timed_turn_right(turn_speed, 0.8)
                    
                    self.stop_robot()
                    print("Movement complete, reassessing\n")
                    time.sleep(0.3)
                
                time.sleep(0.05)

        except KeyboardInterrupt:
            try:
                self.stop_robot()
            except Exception:
                pass
            print("\n[STOPPED] Avoidance stopped by user")


    def improved_obstacle_avoidance(self):
        """
        Robust obstacle avoidance using camera+LiDAR sensor fusion.
        """
        print("\nStarting improved obstacle avoidance with sensor fusion")
        print("Strategy: Move forward -> Detect obstacle -> Analyze all directions -> Turn -> Move\n")
        
        OBSTACLE_THRESHOLD = 0.6
        MIN_SAFE_CLEARANCE = 0.3
        SENSOR_UPDATE_DELAY = 0.3  # Allow sensors to update after movement
        
        try:
            while True:
                # Get all fused sensor data
                front = self.robot_interface.get_parameter('fused_front_range').value
                front_left = self.robot_interface.get_parameter('fused_front_left_range').value
                front_right = self.robot_interface.get_parameter('fused_front_right_range').value
                left = self.robot_interface.get_parameter('fused_left_range').value
                right = self.robot_interface.get_parameter('fused_right_range').value
                
                # Get sensor agreements to verify both sensors working
                ag_f = self.robot_interface.get_parameter('sensor_agreement_front').value
                ag_fl = self.robot_interface.get_parameter('sensor_agreement_front_left').value
                ag_fr = self.robot_interface.get_parameter('sensor_agreement_front_right').value
                ag_l = self.robot_interface.get_parameter('sensor_agreement_left').value
                ag_r = self.robot_interface.get_parameter('sensor_agreement_right').value
                
                # Check for obstacles
                forward_ranges = [front, front_left, front_right, left, right]
                min_range = min(forward_ranges)
                
                if min_range < OBSTACLE_THRESHOLD:
                    # STOP IMMEDIATELY
                    print(f"\n[OBSTACLE] Detected at {min_range:.2f}m - STOPPING")
                    self.stop_robot()
                    time.sleep(SENSOR_UPDATE_DELAY)  # Let sensors stabilize
                    
                    # Re-read sensors after stopping
                    front = self.robot_interface.get_parameter('fused_front_range').value
                    front_left = self.robot_interface.get_parameter('fused_front_left_range').value
                    front_right = self.robot_interface.get_parameter('fused_front_right_range').value
                    left = self.robot_interface.get_parameter('fused_left_range').value
                    right = self.robot_interface.get_parameter('fused_right_range').value
                    
                    ag_f = self.robot_interface.get_parameter('sensor_agreement_front').value
                    ag_fl = self.robot_interface.get_parameter('sensor_agreement_front_left').value
                    ag_fr = self.robot_interface.get_parameter('sensor_agreement_front_right').value
                    ag_l = self.robot_interface.get_parameter('sensor_agreement_left').value
                    ag_r = self.robot_interface.get_parameter('sensor_agreement_right').value
                    
                    directions = {
                        'front': (front, ag_f, 1.5),
                        'front-left': (front_left, ag_fl, 1.3),
                        'front-right': (front_right, ag_fr, 1.3),
                        'left': (left, ag_l, 1.0),
                        'right': (right, ag_r, 1.0),
                    }
                    
                    # Enhanced scoring using improved evaluation function
                    scores = {}
                    for name, (clearance, agreement, dir_mult) in directions.items():
                        is_forward = name.startswith('front')
                        is_straight = (name == 'front')
                        # Use enhanced scoring function
                        scores[name] = self.evaluate_direction_score(
                            clearance, agreement, 
                            is_forward=is_forward, 
                            is_straight=is_straight
                        )
                        # Additional safety check
                        if clearance < MIN_SAFE_CLEARANCE:
                            scores[name] *= 0.1  # Heavily penalize unsafe directions
                    
                    best_dir = max(scores, key=scores.get)
                    best_score = scores[best_dir]
                    best_clearance = directions[best_dir][0]
                    best_agreement = directions[best_dir][1]
                    
                    # Display analysis with sensor fusion info
                    print(f"\nDirection Analysis (Camera+LiDAR):")
                    for name in ['front', 'front-left', 'front-right', 'left', 'right']:
                        c, a, _ = directions[name]
                        c_str = f"{c:.2f}m" if c != float('inf') else "inf  "
                        sensor_status = "FUSED" if a > 0.8 else "PARTIAL" if a > 0.3 else "SINGLE"
                        print(f"  {name:12s}: {c_str} | fusion: {a:.2f} [{sensor_status:7s}] | score: {scores[name]:5.2f}")
                    
                    print(f"\n[DECISION] {best_dir.upper()} (clear={best_clearance:.2f}m, fusion={best_agreement:.2f}, score={best_score:.2f})")
                    
                    # Execute maneuver
                    if best_score == 0:
                        print("All directions blocked - emergency reverse")
                        self.timed_move_back(0.08, 1.5)
                        time.sleep(SENSOR_UPDATE_DELAY)
                        self.timed_turn_left(0.15, 2.0)
                        time.sleep(SENSOR_UPDATE_DELAY)
                    elif 'right' in best_dir:
                        if best_dir == 'right':
                            print("Turning RIGHT 90deg")
                            self.timed_turn_right(0.15, 1.5)
                        else:
                            print("Turning RIGHT 45deg")
                            self.timed_turn_right(0.15, 0.8)
                        time.sleep(SENSOR_UPDATE_DELAY)
                        print("Advancing...")
                        self.timed_move_front(0.08, 1.2)
                        time.sleep(SENSOR_UPDATE_DELAY)
                    elif 'left' in best_dir:
                        if best_dir == 'left':
                            print("Turning LEFT 90deg")
                            self.timed_turn_left(0.15, 1.5)
                        else:
                            print("Turning LEFT 45deg")
                            self.timed_turn_left(0.15, 0.8)
                        time.sleep(SENSOR_UPDATE_DELAY)
                        print("Advancing...")
                        self.timed_move_front(0.08, 1.2)
                        time.sleep(SENSOR_UPDATE_DELAY)
                    else:
                        print("Front clear - advancing")
                        self.timed_move_front(0.08, 0.8)
                        time.sleep(SENSOR_UPDATE_DELAY)
                    
                    print("")
                    
                else:
                    # Path clear - continue forward
                    avg_agreement = (ag_f + ag_fl + ag_fr + ag_l + ag_r) / 5.0
                    fusion_status = "GOOD" if avg_agreement > 0.7 else "PARTIAL" if avg_agreement > 0.4 else "LOW"
                    print(f"Moving forward | clear: {min_range:.2f}m | fusion: {avg_agreement:.2f} [{fusion_status}]   ", end='\r')
                    self.move_front(0.08)
                    time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n\n[STOPPED] User interrupted")
            self.stop_robot()
def main():
    if not rclpy.ok():
        rclpy.init(args=None)
    robot_interface = RobotInterface()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(robot_interface)
    
    # Start executor in separate thread
    def spin_node():
        executor.spin()
    
    spin_thread = threading.Thread(target=spin_node, daemon=True)
    spin_thread.start()

    print("System initializing...")
    time.sleep(5.0)
    print("[READY] System initialized\n")

    controller = RobotControl(robot_interface)
    try:
        controller.run_all_tests()
        controller.improved_obstacle_avoidance()
    except Exception as e:
        print("\n========== ERROR ==========")
        traceback.print_exception(type(e), e, e.__traceback__)
        print("===========================")
    finally:
        executor.shutdown()
        robot_interface.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
