import RPi.GPIO as GPIO
import time

SENSOR_PIN = 2  # GPIO 2

class Sensor:
    """
        LDR control code.
    """

    def __init__(self):
        """Initialize sensor module"""

        self.sensor_pin = SENSOR_PIN

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    def get_state(self):
        return not GPIO.input(self.sensor_pin)

