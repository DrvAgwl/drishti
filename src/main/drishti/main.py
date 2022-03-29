import logging
import os
import signal
import sys
import time
from pathlib import Path

import pigpio

from dotenv import load_dotenv

from src.main.commons.hal.buzzer import Buzzer
from src.main.commons.hal.camera import Camera
from src.main.commons.hal.lcd import Lcd
from src.main.commons.utils.network_utils import get_device_id
from src.main.commons.utils.utils import base_init, is_camera_enabled
from src.main.drishti.api.web import Web
from src.main.drishti.components.inbound import inbound_loop
from src.main.drishti.components.outbound import outbound_loop
from src.main.drishti.components.scanner import BarcodeScanner, BarcodeType
from src.main.drishti.components.weight import WeightCatcher

env_path = Path('/opt/udaan/drishti/src/.env')
load_dotenv(verbose=True, dotenv_path=env_path)
logger = logging.getLogger("drishti_main")


def loop():
    while True:
        if os.getenv('STAGE') == 'OUTBOUND':
            outbound_loop(lcd, barcode_scanner, weight_catcher, buzzer, web_client, camera)
        if os.getenv('STAGE') == 'INBOUND':
            inbound_loop(lcd, barcode_scanner, weight_catcher, buzzer, web_client, camera)


def cleanup():
    buzzer.cleanup()
    pi.stop()
    lcd.close()
    camera.close_camera()


def signal_handler(sig: object, frame: object):
    pi.stop()
    sys.exit(0)


if __name__ == "__main__":
    try:
        pi = pigpio.pi('')
        signal.signal(signal.SIGINT, signal_handler)
        base_init()
        logger.info("Starting Drishti")
        lcd = Lcd(pi, width=20)
        lcd.clear()
        lcd.put_line(0, str(get_device_id()))
        lcd.put_line(1, "Initialising " + os.getenv('STAGE'))
        lcd.put_line(2, "Please Wait")
        weight_catcher = WeightCatcher(lcd)
        buzzer = Buzzer(pi)
        buzzer.switch_off()
        barcode_scanner = BarcodeScanner(lcd)
        if is_camera_enabled():
            camera = Camera(pi, True)
        else:
            camera = None
        # TODO: Move URL to config
        if os.getenv('ENV') == 'DEV':
            web_client = Web("http://10.45.5.5/drishti/fresh-crate-scanner", lcd)
        else:
            web_client = Web("http://10.45.5.6/drishti/fresh-crate-scanner", lcd)

        logger.info("Finished All Init")
        lcd.clear()
        lcd.put_line(1, "Ready " + os.getenv('STAGE'))
        lcd.put_line(2, get_device_id())
    except Exception as e:
        cleanup()
        logger.error("Something went wrong", e)

    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        cleanup()
        logger.error("Loop went wrong", e)
