from time import sleep

from gpiozero import DigitalOutputDevice


class Ringer:
    def __init__(self, ringer_coil_pos_pin, ringer_coil_neg_pin):
        self._ringer_coil_pos_pin = ringer_coil_pos_pin
        self._ringer_coil_neg_pin = ringer_coil_neg_pin

        self._ringer_coil_pos = DigitalOutputDevice(self._ringer_coil_pos_pin)
        self._ringer_coil_neg = DigitalOutputDevice(self._ringer_coil_neg_pin)

    def _off(self):
        self._ringer_coil_pos.off()
        self._ringer_coil_neg.off()

    def _strike(self):
        # push one way
        self._ringer_coil_neg.on()
        self._ringer_coil_pos.off()
        sleep(0.020)

        # pull back
        self._ringer_coil_neg.off()
        self._ringer_coil_pos.on()
        sleep(0.020)

    def ring_burst(self):
        for _ in range(15):
            self._strike()
        self._off()

    def ring_sequence(self, count=1):
        for _ in range(count):
            self.ring_burst()
            sleep(0.1)
            self.ring_burst()
            sleep(4)