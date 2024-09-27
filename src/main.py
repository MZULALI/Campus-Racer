import time
from hardware.servo_controller import ServoController
from hardware.camera import Camera
from hardware.multiplexer import Multiplexer
from autonomous.lane_detection import LaneDetector
from autonomous.path_planning import PathPlanner
from autonomous.controller import AutonomousController
from manual_control.keyboard_control import KeyboardController
from utils.logger import Logger
import threading
import yaml

def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config()
    logger = Logger(config['logging'])
    
    # Initialize hardware
    servo_controller = ServoController(config['servo'])
    camera = Camera(config['camera'])
    multiplexer = Multiplexer(config['multiplexer'])
    
    # Initialize autonomous modules
    lane_detector = LaneDetector(config['autonomous']['lane_detection'])
    path_planner = PathPlanner(config['autonomous']['path_planning'])
    autonomous_controller = AutonomousController(servo_controller, lane_detector, path_planner, logger)
    
    # Initialize manual control
    keyboard_controller = KeyboardController(servo_controller, logger)
    
    # Start camera thread
    camera_thread = threading.Thread(target=camera.start_stream, daemon=True)
    camera_thread.start()
    
    # Start autonomous controller thread
    autonomous_thread = threading.Thread(target=autonomous_controller.run, daemon=True)
    autonomous_thread.start()
    
    # Start manual control in main thread
    try:
        keyboard_controller.run()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        servo_controller.cleanup()
        camera.stop_stream()
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    main()
