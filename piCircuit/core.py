import RPi.GPIO as GPIO
# from .EmulatorGUI import GPIO
from .constants import *

def intTo2Bit(value):
    value = "{0:b}".format(value)
    try:
        v1, v2 = value
    except:
        v2 = value
        v1 = "0"
    return int(v1), int(v2)

class Element():
    global FUNCTION_DICT
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)

    def set2bitValue(self, bit1, bit2):
        GPIO.output(self.pin1, bit1)
        GPIO.output(self.pin2, bit2)

    def setValue(self, value):
        v1, v2 = intTo2Bit(value)
        self.set2bitValue(v1, v2)

    def setFunction(self, function):
        value = FUNCTION_DICT[function]
        self.set2bitValue(*value)
        
    def __del__(self):
		GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
