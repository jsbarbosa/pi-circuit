OPEN = "OPEN"
WIRE = "WIRE"
OP1 = "RLOW"
OP2 = "RHIGH"

FUNCTION_KEYS = [OP1, OPEN, OP2, WIRE]
FUNCTION_VALUES = [(0, 0), (0, 1), (1, 0), (1, 1)]

FUNCTION_DICT = {}
for i in range(4):
    FUNCTION_DICT[FUNCTION_KEYS[i]] = FUNCTION_VALUES[i]

NADC = 6
ADC_NAMES = ["ADC%d"%i for i in range(NADC)]
MAXVAL = 1023

OUT_PINS_PINS = [17, 18, 22, 23, 24, 27]
IN_PINS_PINS = [5, 6, 12, 13, 16, 19]
