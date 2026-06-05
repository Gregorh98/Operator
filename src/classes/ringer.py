from time import sleep

from gpiozero import DigitalOutputDevice


class Ringer:
    def __init__(self, ringer_coil_pos_pin, ringer_coil_neg_pin):
        self._ringer_coil_pos_pin = ringer_coil_pos_pin
        self._ringer_coil_neg_pin = ringer_coil_neg_pin

        self._ringer_coil_pos_pin = DigitalOutputDevice(self._ringer_coil_pos_pin)
        self._ringer_coil_neg_pin = DigitalOutputDevice(self._ringer_coil_neg_pin)

    def _off(self):
        self._ringer_coil_pos_pin.off()
        self._ringer_coil_neg_pin.off()

    def _strike(self):
        # push one way
        self._ringer_coil_neg_pin.on()
        self._ringer_coil_pos_pin.off()
        sleep(0.020)

        # pull back
        self._ringer_coil_neg_pin.off()
        self._ringer_coil_pos_pin.on()
        sleep(0.020)

    def ring(self):
        for _ in range(15):
            self._strike()
        self._off()

