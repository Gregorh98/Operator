from gpiozero import Button

from classes import Ringer, Dial, DialTone, Recorder, Player


class Phone:
    def __init__(self, hook_switch_pin, ringer_coil_pos_pin, ringer_coil_neg_pin, dial_enable_pin, dial_pulse_pin):
        # Ringer and Dial
        self._ringer = Ringer(ringer_coil_pos_pin, ringer_coil_neg_pin)
        self._dial = Dial(dial_enable_pin, dial_pulse_pin, self._on_number_dialed)
        self._dialtone = DialTone()

        # Hook Switch
        self._hook_switch_pin = hook_switch_pin
        self._hook_switch = Button(self._hook_switch_pin, pull_up=True, bounce_time=0.05)

        self._hook_switch.when_pressed = self._phone_placed
        self._hook_switch.when_released = self._phone_lifted

        if not self._hook_switch.is_pressed:
            self._dialtone.start()

        # Recorder
        self._recorder = Recorder(on_finished=self._dialtone.start)
        self._player = Player(on_finished=self._dialtone.start)

        # Startup Event
        self._ringer.ring_sequence()

    def _phone_placed(self):
        print("Phone Placed")
        self._recorder.stop_recording()
        self._player.stop_playing()
        self._dialtone.stop()

    def _phone_lifted(self):
        print("Phone Lifted")
        self._dialtone.start()

    def _on_number_dialed(self, number):
        self._dialtone.stop()

        match number:
            case 1:
                self._recorder.start_recording()
                return
            case 2:
                self._player.play_all_recordings()
                return
            case 9:
                self._ringer.ring_sequence()
            case 0:
                self._player.play_file("operator.wav")

        self._dialtone.start()