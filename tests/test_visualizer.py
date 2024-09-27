# tests/test_visualizer.py

import unittest
from autonomous.visualizer import Visualizer
import numpy as np
import cv2

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        config = {
            'lane_color': [0, 255, 0],
            'lane_thickness': 2,
            'path_color': [0, 0, 255],
            'path_thickness': 2,
            'path_length': 100
        }
        self.visualizer = Visualizer(config)
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def test_draw_lanes(self):
        lanes = [
            [[100, 480, 200, 300]],
            [[540, 480, 440, 300]]
        ]
        frame_with_lanes = self.visualizer.draw_lanes(self.frame.copy(), lanes)
        # Check if lines are drawn by verifying pixel colors
        self.assertTrue(np.any(frame_with_lanes[:, :, 1] > 0), "Lane lines should be drawn in green.")

    def test_draw_path(self):
        steering_angle = 15
        frame_with_path = self.visualizer.draw_path(self.frame.copy(), steering_angle, 30)
        # Check if path line is drawn by verifying pixel colors
        self.assertTrue(np.any(frame_with_path[:, :, 2] > 0), "Path line should be drawn in red.")

    def test_display_frame(self):
        # Since display_frame opens a window, itll mock it to avoid GUI interaction
        #I hope this works
        try:
            import sys
            from unittest.mock import patch
            with patch('cv2.imshow') as mocked_imshow, patch('cv2.waitKey') as mocked_waitkey:
                mocked_waitkey.return_value = ord('q')
                self.visualizer.display_frame(self.frame)
                mocked_imshow.assert_called_once()
                mocked_waitkey.assert_called_once()
                self.assertTrue(True)
        except Exception as e:
            self.fail(f"display_frame raised an exception {e}")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
