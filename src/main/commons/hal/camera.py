import datetime
import logging
import os
import time
from datetime import datetime

import pigpio, picamera

from src.main.commons.hal.led import Led
from src.main.commons.utils.utils import base_init

logger = logging.getLogger("drishti_camera")


class Camera:
    def __init__(self, pi, use_lib=False):
        self.pi = pi
        self.open = False
        self.led = Led(pi)
        self.led.change_brightness(0)
        self.use_lib = use_lib
        if self.use_lib:
            self.camera = picamera.PiCamera()
            self.camera.resolution = (4056, 3040)
            self.camera.start_preview()
            ##Open camera for 2secs, get settings and then freeze them
            time.sleep(2)
            self.camera.shutter_speed = self.camera.exposure_speed
            self.camera.exposure_mode = 'off'
            g = self.camera.awb_gains
            self.camera.awb_mode = 'off'
            self.camera.awb_gains = g

    logger.info("Camera Init")

    def open_camera(self):
        self.led.change_brightness(100)
        self.open = True

    def capture(self):
        start_time = time.time()
        now = datetime.now()
        self.open_camera()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        logger.debug("Capturing Image")
        image_path = '/opt/udaan/drishti/data/%s.jpg' % date_time
        if self.use_lib:
            self.camera.capture(image_path)
        else:
            camera_cmd = "raspistill -t 1000 --awb fluorescent -o " + image_path
            os.system(camera_cmd)
        logger.info("Camera Capture time: " + str(time.time() - start_time))
        return image_path

    def close_leds(self):
        self.led.change_brightness(0)

    def close_camera(self):
        if self.use_lib:
            self.camera.close()

    def clean_image(self, image_path):
        os.remove(image_path)


if __name__ == "__main__":
    base_init()
    pi = pigpio.pi()
    camera = Camera(pi, True)
    i = 0
    camera.open_camera()
    while i < 5:
        image_path = camera.capture()
        # camera.clean_image(image_path)
        i = i + 1

    camera.close_camera()
