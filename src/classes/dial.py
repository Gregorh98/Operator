from gpiozero import Button


class Dial:
    def __init__(self, dial_enable_pin, dial_pulse_pin):
        self._dial_enable = Button(dial_enable_pin, pull_up=True, bounce_time=0.02)
        self._dial_pulse = Button(dial_pulse_pin, pull_up=True, bounce_time=0.01)

        self._dial_pulse.when_pressed = self._pulse
        self._dial_enable.when_released = self._end_digit  # dial stopped moving

        self._pulse_count = 0
        self._buffer = []

    def _pulse(self):
        # only count while dial is active
        if not self._dial_enable.is_pressed:
            return

        self._pulse_count += 1

    def _end_digit(self):
        # dial has stopped moving → convert pulses to digit
        if self._pulse_count == 0:
            return

        digit = 0 if self._pulse_count == 10 else self._pulse_count

        self._buffer.append(digit)
        print("Dialed:", digit)

        self._pulse_count = 0

    def get_number(self):
        return self._buffer