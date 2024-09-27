import sys
import termios
import tty
import time

class KeyboardController:
    def __init__(self, servo_controller, logger):
        self.servo = servo_controller
        self.logger = logger
        self.running = False
    
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    def run(self):
        self.running = True
        self.logger.info("Manual control started. Use W/S for throttle, A/D for steering, and Q to quit.")
        print("Manual control started. Use W/S for throttle, A/D for steering, and Q to quit.")
        while self.running:
            key = self.get_key()
            if key == 'w':
                self.servo.set_throttle(1.0)
                self.logger.info("Throttle: Forward")
            elif key == 's':
                self.servo.set_throttle(-1.0)
                self.logger.info("Throttle: Reverse")
            elif key == 'a':
                self.servo.set_steering(-45)
                self.logger.info("Steering: Left")
            elif key == 'd':
                self.servo.set_steering(45)
                self.logger.info("Steering: Right")
            elif key == ' ':
                self.servo.set_throttle(0.0)
                self.servo.set_steering(0)
                self.logger.info("Throttle and Steering: Neutral")
            elif key == 'q':
                self.running = False
                self.logger.info("Exiting manual control.")
                print("Exiting manual control.")
            print(f"Steering: {self.servo.kit.servo[self.servo.steering_channel].angle}, Throttle: {self.servo.kit.continuous_servo[self.servo.throttle_channel].throttle}")
            time.sleep(0.1)
