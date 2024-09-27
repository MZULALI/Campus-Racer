# src/autonomous/controller.py

import time
from .visualizer import Visualizer
import yaml

class AutonomousController:
    def __init__(self, servo_controller, lane_detector, path_planner, logger, camera):
        self.servo = servo_controller
        self.lane_detector = lane_detector
        self.path_planner = path_planner
        self.logger = logger
        self.camera = camera
        self.running = False

        # Load visualization config
        with open('src/autonomous/visualization_config.yaml', 'r') as file:
            self.visual_config = yaml.safe_load(file)
        self.visualizer = Visualizer(self.visual_config)

    def run(self):
        self.running = True
        while self.running:
            frame = self.get_frame()
            if frame is not None:
                lanes = self.lane_detector.detect_lanes(frame)
                steering_angle = self.path_planner.plan_path(lanes, frame.shape[1])
                self.servo.set_steering(steering_angle)
                self.servo.set_throttle(0.5)  # Constant throttle
                self.logger.info(f"Steering Angle: {steering_angle}")

                frame = self.visualizer.draw_lanes(frame, lanes)
                frame = self.visualizer.draw_path(frame, steering_angle, self.path_planner.max_steering_angle)
                self.visualizer.display_frame(frame)
            else:
                self.logger.warning("No frame received from camera.")
            time.sleep(0.1)

    def get_frame(self):
        # Integrate with camera module to retrieve the latest frame
        if self.camera.running:
            return self.camera.camera.read()
        return None

    def stop(self):
        self.running = False
