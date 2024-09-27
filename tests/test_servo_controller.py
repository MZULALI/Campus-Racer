import unittest
from hardware.servo_controller import ServoController

class TestServoController(unittest.TestCase):
    def setUp(self):
        config = {
            'i2c_address': 0x40,
            'steering_channel': 0,
            'throttle_channel': 1,
            'steering_gain': -0.65,
            'steering_offset': 0,
            'throttle_gain': 0.8
        }
        self.servo = ServoController(config)
    
    def test_set_steering(self):
        try:
            self.servo.set_steering(90)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"set_steering raised an error {e}")
    
    def test_set_throttle(self):
        try:
            self.servo.set_throttle(0.5)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"set_throttle raised an error, probably a (-) like last time :| {e}")
    
    def tearDown(self):
        self.servo.cleanup()

if __name__ == '__main__':
    unittest.main()
