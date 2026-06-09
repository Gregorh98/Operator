from signal import pause

from classes import Phone

HOOK_SWITCH_PIN = 7
RINGER_COIL_POS_PIN = 24
RINGER_COIL_NEG_PIN = 25
DIAL_ENABLE_PIN = 29
DIAL_PULSE_PIN = 28

if __name__ == "__main__":
    print("Running")
    phone = Phone(HOOK_SWITCH_PIN, RINGER_COIL_POS_PIN, RINGER_COIL_NEG_PIN, DIAL_ENABLE_PIN, DIAL_PULSE_PIN)
    phone.ring() # Make phone ring to show script has started
    pause()