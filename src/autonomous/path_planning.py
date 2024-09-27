# src/autonomous/path_planning.py

import numpy as np

class PathPlanner:
    def __init__(self, config):
        self.lookahead_distance = config['lookahead_distance']
        self.max_steering_angle = config['max_steering_angle']
        self.kp = config.get('kp', 0.5)
        self.ki = config.get('ki', 0.0)
        self.kd = config.get('kd', 0.1)
        self.previous_error = 0.0
        self.integral = 0.0

    def plan_path(self, lanes, frame_width):
        # Improved for the time being, TODO: 
        if lanes is None:
            return 0

        left_lines, right_lines = self.separate_lanes(lanes, frame_width)
        left_avg = self.average_slope_intercept(left_lines)
        right_avg = self.average_slope_intercept(right_lines)

        if left_avg is not None and right_avg is not None:
            midpoint = (left_avg[1] + right_avg[1]) / 2
        elif left_avg is not None:
            midpoint = left_avg[1] + self.lookahead_distance
        elif right_avg is not None:
            midpoint = right_avg[1] - self.lookahead_distance
        else:
            midpoint = frame_width / 2

        desired_position = frame_width / 2
        error = desired_position - midpoint
        self.integral += error
        derivative = error - self.previous_error
        self.previous_error = error

        steering_angle = self.kp * error + self.ki * self.integral + self.kd * derivative
        steering_angle = np.clip(steering_angle, -self.max_steering_angle, self.max_steering_angle)

        return steering_angle

    def separate_lanes(self, lanes, frame_width):
        left_lines = []
        right_lines = []
        for line in lanes:
            for x1, y1, x2, y2 in line:
                if x2 - x1 == 0:
                    continue  # avoid division by zero
                slope = (y2 - y1) / (x2 - x1)
                if slope < -0.5:
                    left_lines.append(line)
                elif slope > 0.5:
                    right_lines.append(line)
        return left_lines, right_lines

    def average_slope_intercept(self, lines):
        if len(lines) == 0:
            return None
        slopes = []
        intercepts = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x2 - x1 == 0:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1
                slopes.append(slope)
                intercepts.append(intercept)
        if len(slopes) == 0:
            return None
        slope_avg = np.mean(slopes)
        intercept_avg = np.mean(intercepts)
        y = self.lookahead_distance
        x = (y - intercept_avg) / slope_avg
        return (x, y)
