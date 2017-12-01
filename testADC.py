from time import sleep
import piCircuit as pc

port = pc.Serial(port = '/dev/ttyAMA0')

while True:
	port.printCurrent(0.1)
