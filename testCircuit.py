
from time import sleep
from piCircuit import exampleCircuit as pc

E1 = pc.Element(6, 12)
E2 = pc.Element(16, 19)
while True:
	E1.setFunction("OPEN")
	E2.setFunction("OPEN")
	sleep(2.5)

#~ while True:
    #~ for i in range(4):
        #~ for element in pc.ELEMENTS:
            #~ print(i)
            #~ element.setValue(i)
            #~ sleep(0.5)
