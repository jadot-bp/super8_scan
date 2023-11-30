# Super 8 Helper

Utility code for controlling frame advance and shutter release for scanning Super 8 film.

## Documentation

TBD


## Authors

- [@jadot-bp](https://www.github.com/jadot-bp)


## Dependencies

The following packages are required for installation:

- [gphoto]
- [python-gphoto]
- [RPI.GPIO]

## Hardware

TBD

## Installation

TBD

```bash
  TBD
```

## GPIO Arrangement

This program is designed to interface with the Raspberry Pi GPIO. The (suggested) pin arrangement is as follows:

- Pin 1  -- 3.3V (LED Power)
- Pin 2  -- 5V (Stepper Motor Power)
- Pin 3  -- GPIO 2 (LDR Sense)
- Pin 6  -- GND (LED Ground)
- Pin 7  -- GPIO 4 (Stepper Board IN2)
- Pin 9  -- GND (LDR Ground)
- Pin 11 -- GPIO 17 (Stepper Board IN4)
- Pin 14 -- GND (Stepper Motor Ground)
- Pin 16 -- GPIO 23 (Stepper Board IN1)
- Pin 17 -- 3.3V (LDR Power)
- Pin 18 -- GPIO 24 (Stepper Board IN 3)

Changes to the suggested pin arrangement will require updating the assigned pins in the codebase.
