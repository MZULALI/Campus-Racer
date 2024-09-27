import cv2
import time
from jetcam.usb_camera import USBCamera

class Camera:
    def __init__(self, config):
        self.width = config['resolution'][0]
        self.height = config['resolution'][1]
        self.framerate = config['framerate']
        self.flip_method = config['flip_method']
        self.camera = USBCamera(width=self.width, height=self.height, capture_width=self.width, capture_height=self.height, capture_fps=self.framerate)
        self.running = False
    
    def start_stream(self):
        self.running = True
        while self.running:
            frame = self.camera.read()
            if frame is not None:
                cv2.imshow('Camera Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop_stream()
    
    def stop_stream(self):
        self.running = False
        cv2.destroyAllWindows()
