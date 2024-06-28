from bipolar import Motor
from camera import Camera
from sensor import Sensor

import sys
import RPi.GPIO as GPIO

import time


def advance(pins,outputs,delay):
    # Turn motors
    for pin,state in zip(pins,outputs):    
        if state == 1:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
    time.sleep(delay)

def main(camera_active=False):
    """Scanner controller main wrapper."""

    MOT_DELAY = 0.0025    # Stepper motor delay.
    STEP = 404          # Number of steps to advance per sprocket
    TENSION_STEP_COUNT = 10 # Number of steps to advance takeup spool to maintain tension
    CONTACT_DEAD_PERIOD = 50 # Number of steps to wait before reactivating contact sensor

    MAX_FRAMES = 5000 # Maximum number of frames before system exit.

    # GPIO pin ordering for motor
    TAKEUP_ORDER = [0,1,2,3]
    SPROCKET_ORDER = [3,2,1,0]

    # GPIO pin numbers
    SPROCKET_GPIO = [11,8,9,25]
    TAKEUP_GPIO = [26,20,19,16]

    pins = [*SPROCKET_GPIO,*TAKEUP_GPIO]

    GPIO.setmode(GPIO.BCM) 
    
    # Initialise camera module
    if camera_active:
        camera = Camera()

    # Initialise contact sensor
    sensor = Sensor()

    # Initialise motors

    sprocket = Motor(SPROCKET_ORDER, SPROCKET_GPIO)   # Sprocket puller motor 
    takeup = Motor(TAKEUP_ORDER, TAKEUP_GPIO)     # Takeup spool motor

    # Initialise GPIO

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW) 

    # Begin stepping

    snap_count = 1
    frame_count = 0
    sprocket_step_count = 400
    sprocket_steps = []

    while frame_count < MAX_FRAMES:
        try:

            # check state of contact sensor
            state = sensor.get_state()

            if state and sprocket_step_count > CONTACT_DEAD_PERIOD:   # Claw cam at start of cycle
               
                sprocket_steps.append(sprocket_step_count)
                sprocket_step_count = 0

                for step in range(TENSION_STEP_COUNT):
                    tkup_seq = takeup.step()

                    # Only advance takeup motor
                    outputs = [0,0,1,1,*tkup_seq]

                    advance(pins, outputs, MOT_DELAY)

                # capture
                if camera_active:
                    camera.capture()
                    snap_count += 1

                print("Mean steps: {:.2f}".format(sum(sprocket_steps)/len(sprocket_steps)))
                frame_count += 1

            else:
                sprk_seq = sprocket.step()
                tkup_seq = takeup.step()

                outputs = [*sprk_seq,*tkup_seq]
                advance(pins, outputs,MOT_DELAY)
            
            sprocket_step_count += 1

        except KeyboardInterrupt:
            GPIO.cleanup()

    GPIO.cleanup()
    
    exit()

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        main(bool(int(sys.argv[1])))
    else:
        main()
