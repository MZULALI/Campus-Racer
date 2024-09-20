import cv2
import numpy as np
import threading
import time
import sys
import termios
import tty
import busio
import board
from adafruit_pca9685 import PCA9685

# Function to get keyboard input
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Initialize I2C bus and PCA9685
i2c_bus = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50  # 50Hz for servo control

# Define channels for steering and throttle
steering_channel = pca.channels[0]
throttle_channel = pca.channels[1]

# Neutral duty cycles (adjust based on your servos)
STEERING_NEUTRAL = 0x7FFF
THROTTLE_NEUTRAL = 0x0000

# Min and Max duty cycles for steering
STEERING_MIN = 0x1FFF
STEERING_MAX = 0xEFFF

# Min and Max duty cycles for throttle
THROTTLE_MIN = 0x0000  # Stop
THROTTLE_MAX = 0xFFFF  # Full speed

# Initialize steering and throttle
current_steering = STEERING_NEUTRAL
current_throttle = THROTTLE_NEUTRAL

# Function to update steering and throttle based on key input
def control_loop():
    global current_steering, current_throttle
    print("Control Loop Started. Use WASD keys to control the car. Press 'q' to quit.")
    print("W: Increase Throttle, S: Decrease Throttle, A: Left, D: Right")
    while True:
        key = get_key()
        if key == 'w':
            # Increase throttle
            current_throttle += 0x1000
            if current_throttle > THROTTLE_MAX:
                current_throttle = THROTTLE_MAX
        elif key == 's':
            # Decrease throttle
            current_throttle -= 0x1000
            if current_throttle < THROTTLE_MIN:
                current_throttle = THROTTLE_MIN
        elif key == 'a':
            # Turn left
            current_steering -= 0x1000
            if current_steering < STEERING_MIN:
                current_steering = STEERING_MIN
        elif key == 'd':
            # Turn right
            current_steering += 0x1000
            if current_steering > STEERING_MAX:
                current_steering = STEERING_MAX
        elif key == ' ':
            # Reset to neutral
            current_throttle = THROTTLE_NEUTRAL
            current_steering = STEERING_NEUTRAL
        elif key == 'q':
            # Quit
            break

        # Update servo positions
        steering_channel.duty_cycle = current_steering
        throttle_channel.duty_cycle = current_throttle

        print(f"Steering: {current_steering}, Throttle: {current_throttle}")

    # Stop the car before exiting
    steering_channel.duty_cycle = STEERING_NEUTRAL
    throttle_channel.duty_cycle = THROTTLE_NEUTRAL
    print("Exiting Control Loop.")

# Function to start the camera feed
def camera_loop():
    # Use GStreamer pipeline for CSI camera
    gst_pipeline = ("nvarguscamerasrc ! "
                    "video/x-raw(memory:NVMM), width=(int)640, height=(int)480, "
                    "format=(string)NV12, framerate=(fraction)30/1 ! "
                    "nvvidconv flip-method=2 ! "
                    "video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx ! "
                    "videoconvert ! "
                    "video/x-raw, format=(string)BGR ! appsink")

    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)
    print("Camera Loop Started. Press 'q' in the control window to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display the frame
        cv2.imshow('CSI Camera', frame)
        cv2.waitKey(1)  # This is necessary for the image to display

        # Check if control loop has exited
        if not control_thread.is_alive():
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Exiting Camera Loop.")

# Create and start the control thread
control_thread = threading.Thread(target=control_loop)
control_thread.start()

# Start the camera loop in the main thread
camera_loop()

# Wait for the control thread to finish
control_thread.join()
