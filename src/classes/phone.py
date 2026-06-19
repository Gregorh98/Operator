import json
from time import sleep

import numpy as np
import sounddevice
from gpiozero import Button
from pycparser.c_ast import Switch
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
        self._sr_tone = 8000
        self._phase_350 = 0
        self._phase_450 = 0

        self._dial_tone_stream = sounddevice.OutputStream(
            samplerate=self._sr_tone,
            channels=1,
            dtype="float32",
            callback=self._dial_tone_callback
        )

        if not self._hook_switch.is_pressed:
            self._start_dial_tone()

        # STT
        self._stt_model = Model("vosk_model")
        self._recognizer = KaldiRecognizer(self._stt_model, 16000)

        self._sound_stream = sounddevice.RawInputStream(
            device="USB Audio Device",
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

        sr = self._sr_tone

        # generate sample indices once (fast)
        t = np.arange(frames, dtype=np.float32)

        # compute phase increments
        phase_350 = (self._phase_350 + t) * 2 * np.pi * 350 / sr
        phase_450 = (self._phase_450 + t) * 2 * np.pi * 450 / sr

        outdata[:, 0] = 0.25 * (np.sin(phase_350) + np.sin(phase_450))

        # update phase safely
        self._phase_350 = (self._phase_350 + frames) % sr
        self._phase_450 = (self._phase_450 + frames) % sr

    def _start_dial_tone(self):
        if not self._dial_tone_stream.active:
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
                self._ringer.ring_sequence()
                return

        self._start_dial_tone()

    def ring(self, count=1):
        for _ in range(count):
            self._ringer.ring_sequence()