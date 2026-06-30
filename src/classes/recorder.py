import os
import threading
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime, UTC


class Recorder:
    def __init__(self, sample_frequency=48000, max_recording_duration=30, on_finished=None):
        self._sample_frequency = sample_frequency
        self._max_recording_duration = max_recording_duration

        self._is_recording = False
        self._stop_event = threading.Event()
        self._stream = None
        self._frames = []

        self._on_finished = on_finished

    @property
    def is_recording(self):
        return self._is_recording

    def start_recording(self):
        if self._is_recording:
            return

        print("Recording...")
        self._frames = []
        self._stop_event.clear()
        self._is_recording = True

        def callback(indata, frames, time, status):
            if self._stop_event.is_set():
                raise sd.CallbackStop()
            self._frames.append(indata.copy())

        def _run():
            with sd.InputStream(
                samplerate=self._sample_frequency,
                channels=1,
                dtype="float32",
                callback=callback,
            ):
                self._stop_event.wait(self._max_recording_duration)

            self._stop()

        threading.Thread(target=_run, daemon=True).start()

    def stop_recording(self):
        if not self._is_recording:
            return
        self._stop()

    def _stop(self):
        self._stop_event.set()
        self._is_recording = False
        if self._on_finished is not None:
            self._on_finished()

    def _save_to_file(self):
        print("Saving to file...")

        if not self._frames:
            return

        audio = np.concatenate(self._frames, axis=0)

        timestamp = datetime.now(tz=UTC).isoformat().replace(":", "-")

        os.makedirs("/mnt/usb/recordings", exist_ok=True)
        write(f"/mnt/usb/recordings/{timestamp}.wav", self._sample_frequency, audio)