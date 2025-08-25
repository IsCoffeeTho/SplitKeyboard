import board
import busio
import time

HEARTBEAT_ALIVE = 10
HEARTBEAT_PULSES = 3
HEARTBEAT_DEAD = HEARTBEAT_ALIVE * HEARTBEAT_PULSES

class K_Link_Host:
	def __init__(self, tx, rx, offset=(0,0)):
		self.uart = busio.UART(tx, rx)
		self.offset = offset
		
		self.heartbeat_check_time = 0
		self.heartbeat_drop_count = 0
		self.heartbeat_n = 0
		self.connected = False
		
	def beat_heart(self, now):
		self.connected = True
		self.heartbeat_drop_count = 0
		self.heartbeat_check_time = now + HEARTBEAT_ALIVE
		
	def check_heartbeat(self, now):
		if now > self.heartbeat_check_time:
			self.uart.write(b"H")
			if self.connected:
				if self.heartbeat_drop_count > HEARTBEAT_PULSES:
					self.connected = False
				else:
					self.heartbeat_drop_count += 1
				self.heartbeat_check_time = now + HEARTBEAT_ALIVE
			else:
				self.heartbeat_check_time = now + HEARTBEAT_DEAD
	
	def poll(self, callback):
		now = (time.monotonic() * 1000)
		while self.uart.in_waiting > 0:
			msg_type = self.uart.read(1)
			
			print(msg_type)
			
			if msg_type == b"K":
				if self.uart.in_waiting < 3:
					continue
				self.beat_heart(now)
				x = int.from_bytes(self.uart.read(1))
				y = int.from_bytes(self.uart.read(1))
				state = int.from_bytes(self.uart.read(1))
				callback(x + self.offset[0], y + self.offset[1], state > 0)
				
			if msg_type == b"H":
				self.beat_heart(now)
		self.check_heartbeat(now)
				

class K_Link_Client:
	def __init__(self, tx, rx):
		self.uart = busio.UART(tx, rx)
		self.connected = False
		self.last_ping_time = 0
		
	def send_keydata(self, x, y, state):
		keydata = b"K"
		keydata += x.to_bytes(1)
		keydata += y.to_bytes(1)
		keydata += (b"\x01" if state else b"\x00")
		self.uart.write(keydata)
		
	def check_heartbeat(self, now):
		if now > (self.last_ping_time + HEARTBEAT_DEAD):
			self.connected = False
		
	def poll(self):	
		now = (time.monotonic() * 1000)
		while self.uart.in_waiting > 0:
			msg_type = self.uart.read(1)
			print(msg_type)
			if msg_type == b"H":
				self.connected = True
				self.last_ping_time = now
				self.uart.write(b"H" + self.uart.read(1))
				
		self.check_heartbeat(now)