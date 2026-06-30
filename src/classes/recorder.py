from datetime import datetime, UTC
import threading
import sounddevice as sd
from scipy.io.wavfile import write


class Recorder:
    def __init__(self, sample_frequency=48000, max_recording_duration=30):
        self._sample_frequency = sample_frequency
        self._max_recording_duration = max_recording_duration

        self._is_recording = False
        self._stop_event = threading.Event()
        self._recording = None
        self._thread = None

    @property
    def is_recording(self):
        return self._is_recording

    def start_recording(self):
        print("Recording...")
        if self._is_recording:
            return

        self._is_recording = True
        self._stop_event.clear()

        def _run():
            self._recording = sd.rec(
                int(self._max_recording_duration * self._sample_frequency),
                samplerate=self._sample_frequency,
                channels=1,
                dtype="float32",
            )

            # timer thread: stops after max duration unless already stopped
            timer = threading.Timer(self._max_recording_duration, self.stop_recording)
            timer.start()

            sd.wait()  # blocks until stopped

            timer.cancel()

            if self._recording is not None:
                self._save_to_file(self._recording)

            self._is_recording = False

        self._thread = threading.Thread(target=_run)
        self._thread.start()

    def stop_recording(self):
        if not self._is_recording:
            return

        if self._recording is not None:
            self._save_to_file(self._recording)

        self._stop_event.set()
        sd.stop()  # interrupts sd.rec + sd.wait

    def _save_to_file(self, recording):
        print("Saving to file...")
        timestamp = datetime.now(tz=UTC).isoformat().replace(":", "-")
        write(f"/mnt/usb/{timestamp}.wav", self._sample_frequency, recording)