import motor
from sensor import Sensor
from camera import Camera

import numpy as np
import sys

def main(camera_active=True):
    """Scanner controller main wrapper."""

    MOT_DELAY = 1    # Stepper motor delay.
    ASTEP = 10       # Number of steps to advance per sprocket query.
    CORR_ZONE = 10   # Number of frames to wait before performing sensor
                     # correction.
    MAX_DRIFT = 0.2  # Bound on maximum drift before triggering sensor correction
    SPR_DELAY = 250  # Delay between sensor trigger and shutter release
    MAX_STEPS = 5000 # Maximum number of steps before system exit.

    # Initialize sensor module
    sensor = Sensor()

    # Initialize camera module
    if camera_active:
        camera = Camera()

    ### Begin scanning

    step_counter = 0
    frame_counter = 0    

    last_state = False   # Last sensor state

    shutter_steps = []   # Track steps per frame (shutter release)
    last_shutter = 0     # Steps since last shutter

    while True: 

        # Advance motor
        motor.Advance(MOT_DELAY/1000.0, ASTEP)       

        # Query sprocket presence
        state = sensor.get_state()

        # New sprocket detected
        if state and not last_state:
            ### Shutter release
            motor.Advance(MOT_DELAY/1000.0, SPR_DELAY) 
            
            if camera_active:
                camera.capture()
            else:
                print("Shutter released.")                

            if frame_counter > 0:
                print(f"Frame Captured [{frame_counter}] -- steps = {last_shutter}")
            else:
                print(f"Frame Captured [{frame_counter}]")
            
            frame_counter += 1
            shutter_steps.append(last_shutter)
            last_shutter = 0

        # Trigger on existing sprocket      
        elif state and last_state:
            pass    
 
        # Trigger on end of sprocket
        elif last_state and not state:   
            pass

        # Check for sprocket over-run
        elif not state and not last_state:

            if frame_counter < CORR_ZONE:
                # No sensor correction outside of correction zone.
                pass
 
            elif last_shutter > (1+MAX_DRIFT)*np.median(shutter_steps):
                # Apply sensor correction
                print("Sensor mis-read detected. Capturing frame.")
                
                # Calculate new delay
                new_delay = SPR_DELAY - (last_shutter - np.median(shutter_steps))
                ### Shutter release
                motor.Advance(MOT_DELAY/1000.0, int(new_delay)) 
                
                if camera_active:
                    camera.capture()
                else:
                    print("Shutter released.")

                if frame_counter > 0:
                    print(f"Frame Captured [{frame_counter}] -- steps = {last_shutter}")
                else:
                    print(f"Frame Captured [{frame_counter}]")
                frame_counter += 1
                shutter_steps.append(last_shutter)
                last_shutter = 0

        if last_shutter > MAX_STEPS:
            print(f"No sprocket detected in {MAX_STEPS} steps. Exiting...")
            sys.exit(1)

    
        last_state = state
        step_counter += ASTEP
        last_shutter += ASTEP

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        main(bool(int(sys.argv[1])))
    else:
        main()
