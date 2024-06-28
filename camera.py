#!/usr/bin/env python

import os
import subprocess
import sys

import gphoto as gp


class Camera:
    """
        Camera control module.
    """

    def __init__(self):
        """Initialize camera connection."""
        self.camera = gp.Camera()

    def capture(self):
        self.camera.init()
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        self.camera.exit()
        return 0

    def exit(self):
        return self.camera.exit()

if __name__ == "__main__":
    sys.exit(init())
