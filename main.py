from bipolar import Motor
from camera import Camera

import multiprocessing as mp
import sys
import RPi.GPIO as GPIO

import time

def main(camera_active=False):
    """Scanner controller main wrapper."""

    MOT_DELAY = 1    # Stepper motor delay.
    ASTEP = 10       # Number of steps to advance per sprocket query.
    CORR_ZONE = 10   # Number of frames to wait before performing sensor
                     # correction.
    MAX_DRIFT = 0.2  # Bound on maximum drift before triggering sensor correction
    SPR_DELAY = 250  # Delay between sensor trigger and shutter release
    MAX_STEPS = 5000 # Maximum number of steps before system exit.

    SPROCKET_ORDER = []
    TAKEUP_ORDER = []

    SPROCKET_GPIO = [17,18,27,22]
   # TAKEUP_GPIO = [13,16,19,26]
    
    #SPROCKET_GPIO = [22,27,18,17]
    TAKEUP_GPIO = [26,19,16,13]

    GPIO.setmode(GPIO.BCM) 
    # Initialize camera module
    if camera_active:
        camera = Camera()

    # Initialise motors

    sprocket = Motor(SPROCKET_ORDER, SPROCKET_GPIO)   # Sprocket puller motor 
    takeup = Motor(TAKEUP_ORDER, TAKEUP_GPIO)     # Takeup spool motor

    # Initialise GPIO

    for pin in [*SPROCKET_GPIO,*TAKEUP_GPIO]:
        print(pin)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW) 

    # Begin stepping

    for i in range(200):
        try:   
            outputs = [*sprocket.step(),*takeup.step()]
 
            for pin,state in zip([*SPROCKET_GPIO,*TAKEUP_GPIO],outputs):
            
                print(pin,state)
                if state == 1:
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    GPIO.output(pin, GPIO.LOW)
            time.sleep(0.01)
        except KeyboardInterrupt:
            GPIO.cleanup()
    ### Begin scanning

    step_counter = 0
    frame_counter = 0    

    shutter_steps = []   # Track steps per frame (shutter release)
    last_shutter = 0     # Steps since last shutter

    GPIO.cleanup()
    
    exit()
    while True: 

        # Advance motor

        if camera_active:
            camera.capture()

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        main(bool(int(sys.argv[1])))
    else:
        main()
