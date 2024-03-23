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

        self.position = 0

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

    def step(self):

        #sequence = [[0,0,0,1],[0,1,0,0],[0,0,1,0],[1,0,0,0]]
        sequence = [[0,0,0,1],[0,1,0,1],[0,1,0,0],[0,1,1,0],[0,0,1,0],[1,0,1,0],[1,0,0,0],[1,0,0,1]]

        # Get step in sequence
        output = sequence[self.position] 

        # Move to next step
        self.position += 1

        # Enforce looping of sequence
        if self.position == len(sequence): self.position = 0

        return output
