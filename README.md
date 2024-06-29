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

- [`tkinter`](https://pypi.org/project/tk/)
- [`gphoto`](http://www.gphoto.org/)
- [`python-gphoto`](https://pypi.org/project/gphoto2/0.8.0/)
- [`RPi.GPIO`](https://pypi.org/project/RPi.GPIO/)

## Hardware

This code is designed to work with the following hardware:

- 2x NEMA 17 Stepper Motor
- 2x L298N Motor Driver Module 12V Motor Driver Board
- A `gphoto`-compatible camera of your choice

Please note that any changes to the suggested hardware may result in inconsistent operation. The suggested GPIO arrangement (see below) assumes that the stepper coil arrangement is the same as specified in the 28BYJ-48 datasheet. If using a different stepper motor, please consult the manufacturer's own datasheet.

## Installation

Once the dependencies have been installed, running the Super8 Scanner is as simple as executing the following binary:

```bash
  ./super8_scan
```

## GPIO Arrangement

![GPIO Arrangement](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png)

This program is designed to interface with the Raspberry Pi GPIO. The (suggested) pin arrangement is as follows:

<center>
| Pin No. | Name | Description |
|:---:|:---:| ---|
| Pin 1  | 3.3V | Contact Sensor Power |
| Pin 4  | GPIO 2 | Contact Sensor Sense |
| Pin 21 | GPIO 9 | Stepper L298N IN2 |
| Pin 22 | GPIO 25 | Stepper L298N IN4 |
| Pin 23 | GPIO 11 | Stepper L298N IN1 |
| Pin 24 | GPIO 8 | Stepper L298N IN3 |
| Pin 35 | GPIO 19 | Takeup L298N IN2 |
| Pin 36 | GPIO 16 | Takeup L298N IN4 |
| Pin 37 | GPIO 26 | Takeup L298N IN1 |
| Pin 38 | GPIO 20 | Takeup L298N IN3 |
| Pin 39 | GND | L298N Ground |
</center>

Changes to the suggested pin arrangement will require updating the assigned pins in the code.
