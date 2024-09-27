import unittest
from hardware.camera import Camera
import threading
import time
import cv2

class TestCamera(unittest.TestCase):
    def setUp(self):
        config = {
            'resolution': [640, 480],
            'framerate': 30,
            'flip_method': 2
        }
        self.camera = Camera(config)

    def test_camera_initialization(self):
        self.assertIsNotNone(self.camera.camera, "Camera instance should be initialized.")

    def test_start_stream(self):
        try:
            # Start the camera stream in a separate thread
            def run_stream():
                self.camera.start_stream()

            stream_thread = threading.Thread(target=run_stream)
            stream_thread.start()
            time.sleep(2)  # Let it run 
            self.camera.stop_stream()
            stream_thread.join()
            # Attempt to capture a frame 
            frame = self.camera.camera.read()
            self.assertIsNotNone(frame, "Frame should be captured successfully.")
            self.assertTrue(frame.any(), "Captured frame should contain data.")
        except Exception as e:
            self.fail(f"start_stream raised an error CHECK CONNECTION {e}")

    def tearDown(self):
        self.camera.stop_stream()

if __name__ == '__main__':
    unittest.main()
