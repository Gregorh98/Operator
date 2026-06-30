import sounddevice
import numpy as np

class DialTone:
    def __init__(self):
        self._sr_tone = 48000
        self._phase_350 = 0
        self._phase_450 = 0
        self._enabled = True

        self._dial_tone_stream = sounddevice.OutputStream(
            samplerate=self._sr_tone,
            channels=1,
            dtype="float32",
            blocksize=1024,
            latency="high",
            callback=self._dial_tone_callback
        )

        self._dial_tone_stream.start()

    def start(self):
        self._enabled = True

    def stop(self):
        self._enabled = False

    def _dial_tone_callback(self, outdata, frames, time, status):
        if status.output_underflow:
            print("underflow")

        if not self._enabled:
            outdata.fill(0)
            return

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
