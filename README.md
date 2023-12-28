<img src='/logo.png' width='100'>

# Super 8 Helper

Utility code for controlling frame advance and shutter release for scanning Super 8 film.

This code is in active development and results may vary-- please feel to reach out with any questions!

## Documentation

TBD

## Authors

- [@jadot-bp](https://www.github.com/jadot-bp)

## Dependencies

The following packages are required for installation:

- [`gphoto`](http://www.gphoto.org/)
- [`python-gphoto`](https://pypi.org/project/gphoto2/0.8.0/)
- [`RPi.GPIO`](https://pypi.org/project/RPi.GPIO/)

## Hardware

This code is designed to work with the following hardware:

- LM393 Photosensitive LDR Module
- 28BYJ-48 5V Stepper Motor
- ULN2003 Motor Driver Board
- Generic 3V LED

Please note that any changes to the suggested hardware may result in inconsistent operation. The suggested GPIO arrangement (see below) assumes that the stepper coil arrangement is the same as specified in the 28BYJ-48 datasheet. If using a different stepper motor, please consult the manufacturer's own datasheet. The LDR module must be calibrated with LED to ensure that it activates only when the sprocket passes in front of the detector and that LDR activation also coincides with correct positioning of the film frame in the film gate. Our test setup used a blue LED-- other colours may give differing results.

## Installation

TBD

```bash
  TBD
```

## GPIO Arrangement

![GPIO Arrangement](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png)

This program is designed to interface with the Raspberry Pi GPIO. The (suggested) pin arrangement is as follows:

| Pin No. | Name | Description |
|:---:|:---:| ---|
| Pin 1  | 3.3V | LED Power |
| Pin 2  | 5V | Stepper Motor Power |
| Pin 3  | GPIO 2 | LDR Sense |
| Pin 6  | GND | LED Ground |
| Pin 7  | GPIO 4 | Stepper Board IN2 |
| Pin 9  | GND | LDR Ground |
| Pin 11 | GPIO 17 | Stepper Board IN4 |
| Pin 14 | GND | Stepper Motor Ground |
| Pin 16 | GPIO 23 | Stepper Board IN1 |
| Pin 17 | 3.3V | LDR Power |
| Pin 18 | GPIO 24 | Stepper Board IN 3 |

Changes to the suggested pin arrangement will require updating the assigned pins in the codebase.
