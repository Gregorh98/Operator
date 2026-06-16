import logging

import gpiozero
from gpiozero import Button
from classes import Ringer, Dial
from classes.dial_tone import DialTone
from RealtimeSTT import AudioToTextRecorder


class Phone:
    def __init__(self, hook_switch_pin, ringer_coil_pos_pin, ringer_coil_neg_pin, dial_enable_pin, dial_pulse_pin):
        # Ringer and Dial
        try:
            self._ringer = Ringer(ringer_coil_pos_pin, ringer_coil_neg_pin)
            self._dial = Dial(dial_enable_pin, dial_pulse_pin, self._on_number_dialed)
        except gpiozero.exc.BadPinFactory:
            logging.warning("No GPIO detected")

        # Hook Switch
        self._hook_switch_pin = hook_switch_pin
        self._hook_switch = Button(self._hook_switch_pin, pull_up=True, bounce_time=0.05)

        self._hook_switch.when_pressed = self._phone_placed
        self._hook_switch.when_released = self._phone_lifted

        # Dial Tone
        self._dial_tone = DialTone()
        if not self._hook_switch.is_pressed:
            self._dial_tone.start()

        # STT
        self._recorder = AudioToTextRecorder()

    def _on_word(self, text):
        print(text)

    def _phone_placed(self):
        print("Phone Placed")
        self._dial_tone.stop()

    def _phone_lifted(self):
        print("Phone Lifted")
        self._dial_tone.start()

    def _on_number_dialed(self, number):
        self._dial_tone.stop()

        match(number):
            case 1:
                return
            case 2:
                return
            case 3:
                return
            case 4:
                return
            case 5:
                return
            case 6:
                return
            case 7:
                return
            case 8:
                return
            case 9:
                return
            case 0:
                self.ring()
                return

        self._dial_tone.start()

    def ring(self, count=1):
        for _ in range(count):
            self._ringer.ring_sequence()

    def run(self):
        try:
            while True:
                self._recorder.text(self._on_word)
        except Exception as E:
            print(E)
