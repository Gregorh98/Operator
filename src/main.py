from gpiozero import DigitalOutputDevice, Button

class Phone():
    def __init__(self, hook_switch_pin, ringer_coil_pos_pin, ringer_coil_neg_pin, dial_enable_pin, dial_pulse_pin):
        self._hook_switch_pin = hook_switch_pin
        self._ringer_coil_pos_pin = ringer_coil_pos_pin
        self._ringer_coil_neg_pin = ringer_coil_neg_pin
        self._dial_enable_pin = dial_enable_pin
        self._dial_pulse_pin = dial_pulse_pin

        self._hook_switch = Button(self._hook_switch_pin, pull_up=True)

        