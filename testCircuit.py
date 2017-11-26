
from time import sleep
from piCircuit import exampleCircuit as pc

while True:
    for function in pc.FUNCTION_KEYS:
        for element in pc.ELEMENTS:
            element.setFunction(function)
        sleep(0.5)
