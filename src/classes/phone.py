from gpiozero import Button

from classes import Ringer, Dial


class Phone:
    def __init__(self, hook_switch_pin, ringer_coil_pos_pin, ringer_coil_neg_pin, dial_enable_pin, dial_pulse_pin):
        self._hook_switch_pin = hook_switch_pin
        self._hook_switch = Button(self._hook_switch_pin, pull_up=True)

        self._ringer = Ringer(ringer_coil_pos_pin, ringer_coil_neg_pin)
        self._dial = Dial(dial_enable_pin, dial_pulse_pin)

        self._hook_switch.when_pressed = self._phone_lifted
        self._hook_switch.when_released = self._phone_placed

    def _phone_placed(self):
        print("Phone Placed")

    def _phone_lifted(self):
        print("Phone Lifted")

    def ring(self, count=1):
        for x in range(count):
            self._ringer.ring_sequence()