import logging

import serial

logger = logging.getLogger("drishti_serial")
logger.setLevel(logging.INFO)


class SerialComm:

    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        except Exception as e:
            logger.error("Weighing Scale Not Found", e)
            raise Exception('Serial Scanner Failed')
        self.serial_line = ""

    def read_serial(self):
        serial_data = self.ser.readline().decode('utf-8')
        logger.debug("Read Serial: " + str(serial_data))
        return serial_data

    def close(self):
        self.ser.close()

    def write(self, mssg):
        logger.debug("Writing: " + str(mssg))
        return self.ser.write(mssg)
