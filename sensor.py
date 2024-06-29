import RPi.GPIO as GPIO
import time

SENSOR_PIN = 14  # GPIO 14

class Sensor:
    """
        LDR control code.
    """

    sensor_pin = SENSOR_PIN

    def __init__(self, sensor_pin = None):
        """Initialize sensor module"""
    
        if sensor_pin != None:
            sensor_pin = sensor_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_state(self):
        return GPIO.input(self.sensor_pin)

    def clean_up(self):
        return GPIO.cleanup()
