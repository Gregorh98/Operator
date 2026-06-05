from gpiozero import Button


class Dial:
    def __init__(self, dial_enable_pin, dial_pulse_pin):
        self._dial_enable_pin = dial_enable_pin
        self._dial_pulse_pin = dial_pulse_pin

        self._dial_enable_switch = Button(self._dial_enable_pin, pull_up=True)
        self._dial_pulse_switch = Button(self._dial_pulse_pin, pull_up=True)



