from gpiozero import Button


class Dial:
    def __init__(self, dial_enable_pin, dial_pulse_pin, on_number_event=None):
        self._dial_enable = Button(dial_enable_pin, pull_up=True, bounce_time=0.02)
        self._dial_pulse = Button(dial_pulse_pin, pull_up=True, bounce_time=0.01)

        self._dial_pulse.when_pressed = self._pulse
        self._dial_enable.when_released = self._end_digit  # dial stopped moving

        self._pulse_count = 0
        self._last_digit = None

        if on_number_event:
            self._on_number_event = on_number_event

    def _pulse(self):
        if not self._dial_enable.is_pressed:
            return
        self._pulse_count += 1

    def _end_digit(self):
        if self._pulse_count == 0:
            return

        digit = 0 if self._pulse_count == 10 else self._pulse_count

        self._last_digit = digit
        print("Dialed:", digit)

        self._on_number_event(digit)

        self._pulse_count = 0

    def get_number(self):
        return self._last_digit