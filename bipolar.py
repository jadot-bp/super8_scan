#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

import sys

GPIO.setmode(GPIO.BCM)

class Motor:
    def __init__(self,order, GPIO_pins, forward=True):
        
        self.forward = forward
        self.order = order
        self.GPIO = GPIO_pins

    def setup(self):
        """Initialize pin and push low."""
        GPIO.setwarnings(False)
 
        for pin in self.GPIO:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW) 

    def cleanup(self, flush=False):
        """Push low and clean up."""

        for pin in self.GPIO:
            GPIO.output(pin, GPIO.LOW)

        if flush:
            GPIO.cleanup()  # Clean up GPIO outputs.

    def step(self, step_count, step_sleep):

        out1, out2, out3, out4 = self.GPIO
        pin1, pin2, pin3, pin4 = self.order
        
        for i in range(step_count):
            if i%4==pin1:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==pin2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==pin3:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==pin4:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
     
            time.sleep(step_sleep)

        self.cleanup()
