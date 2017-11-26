# import RPi.GPIO as GPIO
from EmulatorGUI import GPIO
from constants import *

GPIO.setmode(GPIO.BCM)

for key in GPIO_DICT:
    p1, p2 = GPIO_DICT[key]
    GPIO.setup(p1, GPIO.OUT)
    GPIO.setup(p2, GPIO.OUT)

def pinFunction(pin, function):
    number = ELEMENT_DICT[function]
    try:
        v1, v2 = "{0:b}".format(number)
    except:
        v2 = "{0:b}".format(number)
        v1 = "0"
    # print(v1, v2)
    p1, p2 = GPIO_DICT[pin]
    GPIO.output(p1, int(v1))
    GPIO.output(p2, int(v2))

# pinFunction('R1', 'OP2')
