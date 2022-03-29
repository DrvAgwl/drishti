import pigpio
import logging
import time

from src.main.commons.utils.utils import base_init

logger = logging.getLogger("drishti_buzzer")


class Buzzer:
    def __init__(self, pi):
        self.pi = pi
        self.buzzerPin = 4
        self.pi.set_mode(self.buzzerPin, pigpio.OUTPUT)
        self.pi.write(self.buzzerPin, pigpio.LOW)
        logger.info("Buzzer Init")

    def double_beep(self, time_gap=0.2):
        logger.debug("Buzzing Double")
        self.single_beep(time_gap)
        self.single_beep(time_gap)

    def single_beep(self, time_gap=0.2):
        logger.debug("Beeping")
        self.switch_on()
        time.sleep(time_gap)
        self.switch_off()
        time.sleep(time_gap)

    def error_beep(self):
        logger.debug("Beeping error")
        self.single_beep(0.1)
        self.single_beep(0.1)
        self.single_beep(0.1)

    def switch_on(self):
        logger.debug("Buzzing On")
        self.pi.write(self.buzzerPin, pigpio.HIGH)

    def switch_off(self):
        logger.debug("Buzzing OFF")
        self.pi.write(self.buzzerPin, pigpio.LOW)

    def cleanup(self):
        self.switch_off()


def loop():
    while True:
        buzzer.switch_on()
        time.sleep(1)
        buzzer.switch_off()
        time.sleep(1)


if __name__ == "__main__":
    base_init()
    pi = pigpio.pi()
    buzzer = Buzzer(pi)
    buzzer.switch_off()
    try:
        loop()
    except KeyboardInterrupt:
        buzzer.cleanup()
