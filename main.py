import motor
from sensor import Sensor
from camera import Camera

def main(camera_active=True):
    """Scanner controller main wrapper."""

    DELAY = 1        # Stepper motor delay.
    ASTEP = 10          # Number of steps to advance per sprocket query.

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
        motor.Advance(DELAY/1000.0, ASTEP)       

        # Query sprocket presence
        state = sensor.get_state()

        # New sprocket detected
        if state and not last_state:
            ### Shutter release
            motor.Advance(DELAY/1000.0, 250) 
            
            if camera_active:
                camera.capture()
            if frame_counter > 0:
                print(f"Frame Captured [{frame_counter}] -- sp_freq = {sprocket_freqs[-1]}")
            else:
                print(f"Frame Captured [{frame_counter}]")
            #input("Ready?"){}
            frame_counter += 1

        # Trigger on existing sprocket      
        elif state and last_state:
            sp_freq += ASTEP    
        
        # Trigger on end of sprocket
        elif last state and not state   
            # Update sprocket frequency with last reading
            sprocket_freqs.append(sp_freq)
            sp_freq = 0

        last_state = state
        step_counter += ASTEP

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        main(bool(sys.argv[1]))
    else:
        main()
