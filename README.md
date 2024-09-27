# Campus-Racer


Campus Racer is an autonomous RC car project designed to navigate SDSU's red bike lanes using an NVIDIA Jetson Nano, CSI camera, PCA9685 16-channel controller, multiplexer, and RC car components.

For decelopment, I used lane detection via convolutional filters, feature extraction for lane boundaries, and a custom trained model for obstacle avoidance. The racer uses Adafruit's CircuitPython libraries for low level control of the PCA9685 16-channel PWM Servo Motor Driver and multiplexer. 

The stack includes OpenCV for computer vision and JetCam for camera management.

The bike lanes follow through the middle of campus, starting from Hepner Hall and splitting to the Vejas Arena, KPBS, and the Student Union.

Campus Racer will follow the right side of the dotted line, avoiding obsticles and manuvering turns along the way.

## Features

- **Manual Control**: Drive the car using keyboard inputs.
- **Autonomous Driving**: Detect lanes and plan paths to navigate autonomously.
- **Servo and ESC Control**: Precise control of steering and throttle using PWM signals.
- **Multiplexer Management**: Switch between RC control and autonomous control seamlessly.
- **Logging**: Comprehensive logging for monitoring and debugging.


### Prerequisites

- **Hardware**:
  - NVIDIA Jetson Nano 4GB
  - CSI Camera
  - PCA9685 16-channel PWM Servo Motor Driver
  - RC Servo Multiplexer
  - RC Car with Steering Servo and ESC
- **Software**:
  - Python 3.8 or later
  - Required Python libraries 


