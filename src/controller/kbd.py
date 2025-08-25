import usb_hid
from adafruit_hid.keyboard import Keyboard

class splitKeyboard:
	def __init__(self, descriptor=[]):
		self.dev = Keyboard(usb_hid.devices)
		self.descriptor = descriptor
		self.layer = 0
		for y in range(0,len(descriptor)):
			row = descriptor[y]
			for x in range(0, len(row)):
				row[x].parent = self
	
	def handle_key(self, x, y, state):
		key = self.descriptor[y][x]
		if state:
			key.press()
		else:
			key.release()
			
NULL_KBD = splitKeyboard([])

class layerKey:
	def __init__(self, flag):
		self.flag = flag
		self.parent = NULL_KBD
	
	def press(self):
		self.parent.layer = self.parent.layer | self.flag
	
	def release(self):
		self.parent.layer = self.parent.layer & ~self.flag

class key:
	def __init__(self, default=0, layers=[]):
		self.parent = NULL_KBD
		self.default_key = default
		self.layers = layers
		self.layer_pressed = -1
		
	def press(self):
		self.layer_pressed = self.parent.layer
		keycode = self.layers[self.layer_pressed]
		if keycode:
			self.parent.dev.press(keycode)
		elif self.default_key:
			self.parent.dev.press(self.default_key)
	
	def release(self):
		keycode = self.layers[self.layer_pressed]
		if keycode:
			self.parent.dev.release(keycode)
		elif self.default_key:
			self.parent.dev.release(self.default_key)
		self.layer_pressed = -1