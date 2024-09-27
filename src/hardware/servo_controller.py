import time
from adafruit_servokit import ServoKit
import traitlets

class ServoController:
    def __init__(self, config):
        self.kit = ServoKit(channels=16, address=config['i2c_address'])
        self.steering_channel = config['steering_channel']
        self.throttle_channel = config['throttle_channel']
        self.steering_gain = config['steering_gain']
        self.steering_offset = config['steering_offset']
        self.throttle_gain = config['throttle_gain']
    
    def set_steering(self, angle):
        scaled_angle = angle * self.steering_gain + self.steering_offset
        self.kit.servo[self.steering_channel].angle = scaled_angle
        time.sleep(0.1)
    
    def set_throttle(self, throttle):
        self.kit.continuous_servo[self.throttle_channel].throttle = throttle * self.throttle_gain
        time.sleep(0.1)
    
    def cleanup(self):
        self.set_steering(90)
        self.set_throttle(0)
