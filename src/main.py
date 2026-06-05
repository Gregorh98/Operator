from classes import Phone

HOOK_SWITCH_PIN = 4
RINGER_COIL_POS_PIN = 2
RINGER_COIL_NEG_PIN = 3
DIAL_ENABLE_PIN = 22
DIAL_PULSE_PIN = 27

if __name__ == "__main__":
    print("Running")
    phone = Phone(HOOK_SWITCH_PIN, RINGER_COIL_POS_PIN, RINGER_COIL_NEG_PIN, DIAL_ENABLE_PIN, DIAL_PULSE_PIN)
    phone.ring(3)