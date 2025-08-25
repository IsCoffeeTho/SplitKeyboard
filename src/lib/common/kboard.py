import digitalio
import time

class K_Board:
	def __init__(self, rows, cols, offset=(0,0)):
		self.rows = []
		self.cols = []
		self.states = []
		self.offset = offset
		
		# set column pins
		for x in range(0, len(cols)):
			pin = digitalio.DigitalInOut(cols[x])
			pin.switch_to_input(digitalio.Pull.DOWN)
			self.cols.append(pin)
		
		# set row pins
		for y in range(0, len(rows)):
			pin = digitalio.DigitalInOut(rows[y])
			pin.switch_to_output()
			self.rows.append(pin)
			
			# make state table
			row_state = []
			for x in range(0, len(cols)):
				row_state.append(False)
			self.states.append(row_state)
	
	def poll(self, callback):
		updates = []
		for y in range(0, len(self.rows)):
			# turn row on
			self.rows[y].value = True
			# get states of row
			row_state = self.states[y]
			# wait on propagation
			time.sleep(0.0001)
			
			# check columns
			for x in range(0, len(self.cols)):
				state = self.cols[x].value
				# pin has changed
				if not row_state[x] == state:
					# save change
					row_state[x] = state
					# send update
					updates.append((x, y, state))
			# turn row off
			self.rows[y].value = False
		
		for update in updates:
			callback(update[0]+self.offset[0], update[1]+self.offset[1], update[2])