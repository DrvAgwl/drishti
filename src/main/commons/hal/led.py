import pigpio
import time

from src.main.commons.hal.buzzer import Buzzer


class Led:
    def __init__(self, pi):
        self.pi = pi
        self.ledPin = 13
        self.pi.set_mode(self.ledPin, pigpio.OUTPUT)

    def change_brightness(self, brightness=100):
        pwm_duty = brightness / 100 * 255
        self.pi.set_PWM_dutycycle(self.ledPin, pwm_duty)


def cleanup():
    buzzer.switch_off()
    pi.stop()


def loop():
    while True:
        for dc in range(0, 101, 1):
            led.change_brightness(dc)
            buzzer.switch_on()
            time.sleep(0.01)
        time.sleep(1)
        for dc in range(100, -1, -1):
            led.change_brightness(dc)
            buzzer.switch_off()
            time.sleep(0.01)
        time.sleep(1)


if __name__ == "__main__":
    pi = pigpio.pi('')
    buzzer = Buzzer(pi)
    led = Led(pi)
    try:
        loop()
    except KeyboardInterrupt:
        cleanup()
