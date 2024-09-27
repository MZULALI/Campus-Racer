# src/autonomous/visualizer.py

import cv2
import numpy as np

class Visualizer:
    def __init__(self, config):
        self.config = config

    def draw_lanes(self, frame, lanes):
        if lanes is not None:
            for line in lanes:
                for x1, y1, x2, y2 in line:
                    cv2.line(frame, (x1, y1), (x2, y2), self.config['lane_color'], self.config['lane_thickness'])
        return frame

    def draw_path(self, frame, steering_angle, max_steering_angle):
        height, width, _ = frame.shape
        # Calculate the end point based on the steering angle
        angle_rad = np.deg2rad(steering_angle)
        length = self.config['path_length']
        x_end = int(width / 2 + length * np.sin(angle_rad))
        y_end = int(height - length * np.cos(angle_rad))
        cv2.line(frame, (int(width / 2), height), (x_end, y_end), self.config['path_color'], self.config['path_thickness'])
        return frame

    def display_frame(self, frame):
        cv2.imshow('Campus-Racer AI Planning', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()
