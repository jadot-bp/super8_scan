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

    sprocket_freqs = []
    sp_freq = 0

    last_state = False   # Last sensor state

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
                print(f"Frame Captured [{frame_counter}] -- sp_freq = {sprocket_freqs[-1]}")
            else:
                print(f"Frame Captured [{frame_counter}]")
            frame_counter += 1

        # Trigger on existing sprocket      
        elif state and last_state:
            sp_freq += ASTEP    
        
        # Trigger on end of sprocket
        elif last_state and not state   
            # Update sprocket frequency with last reading
            sprocket_freqs.append(sp_freq)
            sp_freq = 0

        # Check for sprocket over-run
        elif not state and not last_state

            if frame_counter < CORR_ZONE:
                pass 
            elif sp_freq > (1+ERR_BOUND)*np.median(sprocket_freqs):
                print("Sensor mis-read detected. Capturing frame.")
                
                # Calculate new delay
                new_delay = SPR_DELAY - (sp_freq - np.median(sprocket_freqs))
                ### Shutter release
                motor.Advance(MOT_DELAY/1000.0, int(new_delay)) 
                
                if camera_active:
                    camera.capture()
                else:
                    print("Shutter released.")

                if frame_counter > 0:
                    print(f"Frame Captured [{frame_counter}] -- sp_freq = {sprocket_freqs[-1]}")
                else:
                    print(f"Frame Captured [{frame_counter}]")
                frame_counter += 1

        if sp_freq > MAX_STEPS:
            print(f"No sprocket detected in {MAX_STEPS} steps. Exiting...")
            sys.exit(1)

    
        last_state = state
        step_counter += ASTEP

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        main(bool(sys.argv[1]))
    else:
        main()
