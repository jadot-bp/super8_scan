import motor
from sensor import Sensor
from camera import Camera

import numpy as np
import pandas as pd

def main():
    """Scanner controller main wrapper."""

    DELAY = 0.8        # Stepper motor delay.
    ASTEP = 10          # Number of steps to advance per sprocket query.

    # Initialize sensor module
    sensor = Sensor()

    # Initialize camera module
    camera = Camera()

    ### Begin scanning

    step_counter = 0
    frame_counter = 0    

    sprocket_freqs = []
    sp_freq = 0

    last_state = None   # Last sensor state

    while True: 

        # Advance motor
        motor.Advance(DELAY/1000.0, ASTEP)       

        # Query sprocket presence
        state = sensor.get_state()

        if state:
            ### Sprocket detected

            if last_state:
                sp_freq += ASTEP    
            else:    
                ### Shutter release
                motor.Advance(DELAY/1000.0, 50) 
                camera.capture()
                print(f"Frame Captured [{frame_counter}]")
                frame_counter += 1
        else:
            if last_state:
                # Update sprocket frequency with last reading
                sprocket_freqs.append(sp_freq)
                sp_freq = 0

        last_state = state
        step_counter += ASTEP

        output = np.asarray(sprocket_freqs)
        
        np.savetxt('output.csv', output, delimiter=',')

if __name__ == "__main__":
    main()
