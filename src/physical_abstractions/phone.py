from gpiozero import Button

from features import DialTone, Recorder, Player
from physical_abstractions import Ringer, Dial
from physical_abstractions.hookswitch import HookSwitch


class Phone:
    def __init__(self, hook_switch_pin, ringer_coil_pos_pin, ringer_coil_neg_pin, dial_enable_pin, dial_pulse_pin):
        # Setup
        self._setup_physical_abstractions(hook_switch_pin, ringer_coil_pos_pin, ringer_coil_neg_pin, dial_enable_pin, dial_pulse_pin)
        self._setup_features()
        self._setup_programs()

        # Startup
        self._startup()

    # region Setup
    def _startup(self):
        if not self._hook_switch.is_pressed:
            self._dialtone.start()

        self._ringer.ring_sequence()

    def _setup_physical_abstractions(self, hook_switch_pin: int, ringer_coil_pos_pin: int, ringer_coil_neg_pin: int, dial_enable_pin: int, dial_pulse_pin: int) -> None:
        """
        This method sets up programmatic versions of the physical hardware of the telephone. These include the ringer, dial, and hook switch.
        :param hook_switch_pin: The pin number of the hook switch used to hang the phone up.
        :param ringer_coil_pos_pin: The pin number of the positive terminal of the ringer coil used to make the phone ring.
        :param ringer_coil_neg_pin: The pin number of the negative terminal of the ringer coil used to make the phone ring.
        :param dial_enable_pin: The pin number of the switch that activates when the rotary dial begins to move.
        :param dial_pulse_pin: The pin number of the switch that pulses when the dial returns from a number to rest to count the number selected.
        :return: None
        """
        # Ringer and Dial
        self._ringer = Ringer(ringer_coil_pos_pin, ringer_coil_neg_pin)
        self._dial = Dial(dial_enable_pin, dial_pulse_pin, self._on_number_dialed)
        self._hook_switch = HookSwitch(hook_switch_pin, self._phone_placed, self._phone_lifted)

    def _setup_features(self) -> None:
        """
        Set up the non-physical features of the telephone (dialtone, recorder, player etc)
        :return: None
        """
        self._dialtone = DialTone()
        self._recorder = Recorder(on_finished=self._dialtone.start)
        self._player = Player(on_finished=self._dialtone.start)

    def _setup_programs(self) -> None:
        """
        Set up the programs that can be run.
        :return: None
        """
        # self._dialtone_program = DialToneProgram()
        return

    # endregion

    # region Events
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
            case 0:
                self._player.play_file("operator.wav")
            case _:
                self._ringer.ring_sequence()

        self._dialtone.start()

    #endregion