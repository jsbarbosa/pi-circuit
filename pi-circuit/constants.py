
GPIO_KEYS = ['R1', 'R2', 'R3', 'R4', 'R5', 'LED']
ELEMENT_KEYS = ['OPEN', 'WIRE', 'OP1', 'OP2']

GPIO_DICT = {
    GPIO_KEYS[0]: (2, 3),
    GPIO_KEYS[1]: (5, 6),
    GPIO_KEYS[2]: (9, 10),
    GPIO_KEYS[3]: (14, 15),
    GPIO_KEYS[4]: (20, 21),
    GPIO_KEYS[5]: (23, 24)
}


ELEMENT_DICT = {}
for i in range(4):
    ELEMENT_DICT[ELEMENT_KEYS[i]] = i
