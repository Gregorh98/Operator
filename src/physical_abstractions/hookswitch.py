from gpiozero import Button


class HookSwitch:
    def __init__(self, hook_switch_pin, on_pressed_event=None, on_released_event=None):
        self._hook_switch = Button(hook_switch_pin, pull_up=True, bounce_time=0.05)

        if on_pressed_event:
            self._hook_switch.when_pressed = on_pressed_event

        if on_released_event:
            self._hook_switch.when_released = on_released_event

    @property
    def is_pressed(self):
        return self._hook_switch.is_pressed

    @property
    def is_released(self):
        return not self.is_pressed