import serial
from time import sleep
from codecs import decode
from threading import Thread

BAUDRATE = 4800
TIMEOUT = 1.0

class Serial(serial.Serial):
	def __init__(self, port):
		super().__init__(port = port, baudrate = BAUDRATE, timeout = TIMEOUT,
		stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE,
                        bytesize = serial.EIGHTBITS,)
		
		self.channel0 = 0
		self.channel1 = 0
		self.channel2 = 0
		self.channel3 = 0
		self.channel4 = 0
		self.channel5 = 0
		
		self.vals = [getattr(self, "channel%d"%i) for i in range(6)]
		
		self.thread = Thread(target = self.loop)
		self.thread.daemon = True
		self.thread.start()
		
		self.flush()
		self.flushInput()
		
	def readline(self):
		line = b""
		while True:
			byte = self.read(1)
			if byte == b'\n':
				break
			else:
				line += byte

		line = str(line)[2:-1]
		line = line.replace(r"\x", "")
		try:
			if len(line) == 6:
				channel = int(line[:2], 16)
				value = line[2:]
				value = int(value, 16)
				if value <= 1023:
					return channel, value
		except:
			pass
			
		return -1, 0
		
	def loop(self):
		while True:
			ch, val = self.readline()
			if ch >= 0 and ch <= 5:
				setattr(self, "channel%d"%ch, val) 
			sleep(0.001)
			
	def printCurrent(self, refresh):
		self.vals = [getattr(self, "channel%d"%i) for i in range(6)]
		print(chr(27) + "[2J")
		print(self.vals)
		sleep(refresh)
        
	def getCurrentValues(self):
		self.vals = [getattr(self, "channel%d"%i) for i in range(6)]
		return self.vals
    
	def getCurrentChannel(self, channel):
		return getattr(self, "channel%d"%channel)
