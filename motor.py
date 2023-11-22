import RPi.GPIO as GPIO
import time

# Set GPIO mode

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Assign GPIO pins

coil_A_1_pin = 4        # GPIO 4
coil_A_2_pin = 17       # GPIO 17
coil_B_1_pin = 23       # GPIO 23
coil_B_2_pin = 24       # GPIO 24

# Set up external motor sequence

StepCount = 8
Seq = list(range(0, StepCount))

Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0]
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]

# Initialize GPIO pins

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Define motor utility functions

def SetStep(M1, M2, M3, M4):
    """Sets the magnets M1-4 corresponding to the step."""

    GPIO.output(coil_A_1_pin, M1)
    GPIO.output(coil_A_2_pin, M2)
    GPIO.output(coil_B_1_pin, M3)
    GPIO.output(coil_B_2_pin, M4)

def Advance(delay: float, steps: int):
    """Advance the motor by a given number of steps with specified delay."""
    
    for i in range(steps):
        for j in reversed(range(StepCount)):
            SetStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

def Reverse(delay: float, steps: int):
    """Reverse the motor by a given number of steps with specified delay."""
    
    for i in range(steps):
        for j in range(StepCount):
            SetStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
