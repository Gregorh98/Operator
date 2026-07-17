import sounddevice
import numpy as np

class DialTone:
    def __init__(self, sample_frequency=48000):
        self._sr_tone = sample_frequency

        self._phase_350 = 0
        self._phase_450 = 0
        self._enabled = True
        self._inc350 = 2 * np.pi * 350 / self._sr_tone
        self._inc450 = 2 * np.pi * 450 / self._sr_tone

        self._dial_tone_stream = sounddevice.OutputStream(
            samplerate=self._sr_tone,
            channels=1,
            dtype="float32",
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

        t = np.arange(frames, dtype=np.float32)

        phase_350 = self._phase_350 + self._inc350 * t
        phase_450 = self._phase_450 + self._inc450 * t

        outdata[:, 0] = 0.25 * (np.sin(phase_350) + np.sin(phase_450))

        self._phase_350 = phase_350[-1] + self._inc350
        self._phase_450 = phase_450[-1] + self._inc450
