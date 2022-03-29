import os
import re
import time
from threading import Thread

import pigpio

import logging

from src.main.commons.hal.lcd import Lcd
from src.main.commons.hal.serial_comm import SerialComm
from src.main.commons.utils.utils import base_init

logger = logging.getLogger("drishti_weight")

STABLE_THRESH = 10
READ_STRING = 'bR\n\r'.encode()
TARING_STRING = 'bT\n\rZ\n\r'.encode()


def clean_weight_string(input_weight):
    wt = re.search("[^0-9\-\.]*(\-?\d+\.\d+).*", input_weight)
    if wt is None:
        logger.error("Regex Failed for: " + str(input_weight))
        return ""
    weight = wt.group(1)
    if weight is None:
        logger.error("Group regex failed")
        return ""
    return float(weight)


class WeightCatcher:

    def __init__(self, lcd):
        self.lcd = lcd
        try:
            self.serial_comm = SerialComm()
        except Exception as e:
            logger.error("Weight Scanner Init Failed", e)
            self.lcd.put_line(1, "Weighing Scale Error.")
        logger.info("Weighing Scale: " + os.getenv('MACHINE'))
        self.wait_to_tare = False
        self.weight_to_search = -1
        self.found_count = 0
        self.data_log_count = 0
        self.thread = Thread(target=self.weight_capture_thread)
        self.thread.start()
        self.weight = -1

    def read_weight(self):
        if os.getenv('MACHINE') == "UDAAN":
            self.serial_comm.write(READ_STRING)
        return clean_weight_string(self.serial_comm.read_serial())

    def weight_capture_thread(self):
        logging.debug("Thread %s: starting")
        while True:
            try:
                self.weight = self.read_weight()
            except Exception as e:
                logger.error("Failed reading line", e)
            if self.wait_to_tare:
                logger.debug("Waiting to tare")
                if self.are_similar_weights(self.weight_to_search, self.weight):
                    self.found_count = self.found_count + 1
                    logger.debug("Found: " + str(self.found_count))
                    if self.found_count >= STABLE_THRESH:
                        self.tare_machine()
                        self.wait_to_tare = False
                        self.found_count = 0
            self.data_log_count += 1
            # Reduce logging
            if self.data_log_count % 1000 == 0:
                logging.info("Weight Data: " + str(self.weight))

    def are_similar_weights(self, weight1, weight2):
        # weight1 = clean_weight_string(weight1)
        logger.debug("Comparing Weights F: " + str(weight1) + " S: " + str(weight2))
        val = round(abs(float(weight1) - float(weight2)), 2)
        logger.debug("Val: " + str(val))
        return val <= 0.01

    def get_weight(self):
        logger.debug("Give me weight")
        try:
            weight_reading = self.weight
        except Exception as e:
            logger.error("Weight Reading failed", exc_info=e)
            return -1
        return float(weight_reading)

    def close(self):
        self.serial_comm.close()

    def tare_machine(self):
        logger.info("Starting Taring Weight")
        ##TODO (Soumyadeep): Remove arbit number 5
        for i in range(1, 5):
            self.serial_comm.write(TARING_STRING)

    def delay_and_tare(self, weight_to_search):
        logger.debug("Delay and Tare Started: " + str(self.weight_to_search))
        self.wait_to_tare = True
        self.weight_to_search = weight_to_search

    def reset_delay_and_tare(self):
        self.wait_to_tare = False
        self.weight_to_search = -1


if __name__ == "__main__":
    base_init()
    pi = pigpio.pi('cbtr1.local')
    lcd = Lcd(pi)
    wt_catcher = WeightCatcher(lcd)
    while True:
        time.sleep(3)
        wt_catcher.tare_machine()
        time.sleep(3)
