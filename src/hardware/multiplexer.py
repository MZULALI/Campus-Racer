import time
import RPi.GPIO as GPIO

class Multiplexer:
    def __init__(self, config):
        self.address = config['address']
        self.sel_pins = config['control_pins']['sel']
        GPIO.setmode(GPIO.BCM)
        for pin in self.sel_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
    
    def select_channel(self, channel):
        binary = format(channel, '03b')
        for i, pin in enumerate(self.sel_pins):
            GPIO.output(pin, int(binary[i]))
        time.sleep(0.1)
    
    def cleanup(self):
        GPIO.cleanup()
