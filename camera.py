#!/usr/bin/env python

import os
import subprocess
import sys

import gphoto2 as gp

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
        #print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        #target = os.path.join('/tmp','test.img')
        #print('Copying image to', target)
        #camera_file = self.camera.file_get(
        #    file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        #camera_file.save(target)
        self.camera.exit()
        return 0

    def exit(self):
        return self.camera.exit()

if __name__ == "__main__":
    sys.exit(init())
