import os
import threading
import time

import sounddevice as sd
from scipy.io.wavfile import read


class Player:
    def __init__(self, recordings_directory="/mnt/usb/recordings"):
        self._recordings_directory = recordings_directory
        self._stop_event = threading.Event()
        self._thread = None
        self._is_playing = False

    @property
    def is_playing(self):
        return self._is_playing

    def play_all_recordings(self):
        if self._is_playing:
            return

        self._stop_event.clear()

        def _run():
            self._is_playing = True

            try:
                files = sorted(
                    f for f in os.listdir(self._recordings_directory)
                    if f.lower().endswith(".wav")
                )

                for file_name in files:
                    if self._stop_event.is_set():
                        break

                    self._play_file(os.path.join(self._recordings_directory, file_name))

                    if self._stop_event.is_set():
                        break

                    # Wait 2 seconds between clips, but allow interruption
                    if self._stop_event.wait(2):
                        break

            finally:
                self._is_playing = False

        self._thread = threading.Thread(target=_run)
        self._thread.start()

    def _play_file(self, file_name):
        sample_rate, audio = read(file_name)

        sd.play(audio, sample_rate)

        # Wait until playback finishes, unless stopped
        while sd.get_stream().active:
            if self._stop_event.wait(0.1):
                sd.stop()
                break

    def stop_playing(self):
        if not self._is_playing:
            return

        self._stop_event.set()
        sd.stop()

        if self._thread is not None:
            self._thread.join()