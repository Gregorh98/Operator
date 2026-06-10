import json
from time import sleep

import numpy as np
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

        # Dial Tone
        self._dial_tone_phase = 0
        self._dial_tone_stream = sounddevice.OutputStream(
            samplerate=8000,
            channels=1,
            dtype="float32",
            callback=self._dial_tone_callback
        )

        if not self._hook_switch.is_pressed:
            self._start_dial_tone()

        # STT
        self._stt_model = Model("vosk_model")
        self._recognizer = KaldiRecognizer(self._stt_model, 16000)

        print(sounddevice.query_devices())

        self._sound_stream = sounddevice.RawInputStream(
            device=None,
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._on_word
        )
        self._sound_stream.start()

    def _dial_tone_callback(self, outdata, frames, time, status):
        if status:
            print(status)

        t = np.arange(frames) + self._dial_tone_phase
        tone = 0.3 * np.sin(
            2 * np.pi * 350 * t / 8000
        )
        outdata[:, 0] = tone.astype(np.float32)
        self._dial_tone_phase += frames

    def _start_dial_tone(self):
        if not self._dial_tone_stream.active:
            self._dial_tone_phase = 0
            self._dial_tone_stream.start()

    def _stop_dial_tone(self):
        if self._dial_tone_stream.active:
            self._dial_tone_stream.stop()

    def _on_word(self, indata, frames, time, status):
        if status:
            print(status)

        if self._hook_switch.is_pressed:
            return

        if self._recognizer.AcceptWaveform(bytes(indata)):
            result = json.loads(self._recognizer.Result())
            print(result["text"])

    def _phone_placed(self):
        print("Phone Placed")
        self._stop_dial_tone()

    def _phone_lifted(self):
        print("Phone Lifted")
        self._start_dial_tone()

    def _on_number_dialed(self, number):
        self._stop_dial_tone()

        for _ in range(number):
            self._ringer.ring_burst()
            sleep(0.1)

        self._start_dial_tone()

    def ring(self, count=1):
        for _ in range(count):
            self._ringer.ring_sequence()