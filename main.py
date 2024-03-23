from bipolar import Motor
from camera import Camera

import multiprocessing as mp
import sys
import RPi.GPIO as GPIO

import time

def main(camera_active=False):
    """Scanner controller main wrapper."""

    MOT_DELAY = 0.02    # Stepper motor delay.
    STEP = 41           # Number of steps to advance per sprocket
    SPROCKET_WAIT = 0.4   # Time to wait after sprocket advance
    
    MAX_STEPS = 5000 # Maximum number of steps before system exit.

    # GPIO pin ordering for motor
    SPROCKET_ORDER = [3,2,1,0]
    TAKEUP_ORDER = [3,2,1,0]

    # GPIO pin numbers
    SPROCKET_GPIO = [17,18,27,22]
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

    sprocket_step = 0
    time_count = 0

    for i in range(int(MAX_STEPS*STEP)):
        print(sprocket_step,time_count)
        try:

            # Advance sprocket motor if step not reached   
            if sprocket_step < STEP:
                sprk_seq = sprocket.step()

            # Check if sprocket motor has waited
            if time_count >= SPROCKET_WAIT:
                sprocket_step = 0 
                time_count = 0

            # Advance takeup motor regardless
            tkup_seq = takeup.step()

            if sprocket_step == STEP:
                # Only advance takeup
                pins = [*SPROCKET_GPIO,*TAKEUP_GPIO]
                outputs = [0,0,0,0,*tkup_seq]
            else:        
                pins = [*SPROCKET_GPIO,*TAKEUP_GPIO]
                outputs = [*sprk_seq,*tkup_seq]
 
            for pin,state in zip(pins,outputs):
            
                if state == 1:
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    GPIO.output(pin, GPIO.LOW)

            time.sleep(MOT_DELAY)

            if sprocket_step < STEP:
                sprocket_step += 1
            else:
                time_count += MOT_DELAY
            

        except KeyboardInterrupt:
            GPIO.cleanup()

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
