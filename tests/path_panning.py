# tests/test_path_planning.py

import unittest
from autonomous.path_planning import PathPlanner

class TestPathPlanner(unittest.TestCase):
    def setUp(self):
        config = {
            'lookahead_distance': 50,
            'max_steering_angle': 30,
            'kp': 0.5,
            'ki': 0.1,
            'kd': 0.05
        }
        self.path_planner = PathPlanner(config)

    def test_plan_path_with_no_lanes(self):
        steering_angle = self.path_planner.plan_path(None, 640)
        self.assertEqual(steering_angle, 0, "Steering angle should be 0 when no lanes are detected.")

    def test_plan_path_with_lanes(self):
        # Simulate detected bike lanes 
        # Implement color eventually, maroon? red? TODO
        lanes = [
            [[100, 480, 200, 300]],
            [[540, 480, 440, 300]]
        ]
        steering_angle = self.path_planner.plan_path(lanes, 640)
        self.assertTrue(-30 <= steering_angle <= 30, "Steering angle should be within max steering angle limits.")

    def test_plan_path_with_single_lane(self):
        lanes = [
            [[100, 480, 200, 300]]
        ]
        steering_angle = self.path_planner.plan_path(lanes, 640)
        self.assertTrue(-30 <= steering_angle <= 30, "Steering angle should be within max steering angle limits.")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
