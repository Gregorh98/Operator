import json
from time import sleep

import sounddevice
from gpiozero import Button
from vosk import Model, KaldiRecognizer

from classes import Ringer, Dial



class Phone:
    def __init__(self, hook_switch_pin, ringer_coil_pos_pin, ringer_coil_neg_pin, dial_enable_pin, dial_pulse_pin):
        # Ringer and Dial
        self._ringer = Ringer(ringer_coil_pos_pin, ringer_coil_neg_pin)
        self._dial = Dial(dial_enable_pin, dial_pulse_pin, self._on_number_dialed)

        # Hook Switch
        self._hook_switch_pin = hook_switch_pin
        self._hook_switch = Button(self._hook_switch_pin, pull_up=True, bounce_time=0.05)

        self._hook_switch.when_pressed = self._phone_placed
        self._hook_switch.when_released = self._phone_lifted

        # STT
        self._stt_model = Model("vosk_model")
        self._recognizer = KaldiRecognizer(self._stt_model, 16000)
        sounddevice.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=self._on_word).start()

    def _on_word(self, indata, frames, time, status):
            if self._recognizer.AcceptWaveform(bytes(indata)):
                result = json.loads(self._recognizer.Result())
                print(result["text"])

    def _phone_placed(self):
        print("Phone Placed")

    def _phone_lifted(self):
        print("Phone Lifted")

    def _on_number_dialed(self, number):
        for x in range(number):
            self._ringer.ring_burst()
            sleep(0.1)

    def ring(self, count=1):
        for x in range(count):
            self._ringer.ring_sequence()