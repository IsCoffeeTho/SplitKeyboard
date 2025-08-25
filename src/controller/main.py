import board
import digitalio
import time
from common.kboard import K_Board
from common.klink import K_Link_Host

from cfg import KBD

dev = K_Board(
	rows = (
		board.GP16,
		board.GP17,
		board.GP18,
		board.GP19,
		board.GP20
	),
	cols = (
		board.GP15,
		board.GP14,
		board.GP13,
		board.GP12,
		board.GP11,
		board.GP10
	),
	offset = (6,0)
)

com = K_Link_Host(board.GP0, board.GP1)

led_pin = digitalio.DigitalInOut(board.LED)
led_pin.switch_to_output()

def key_change(x, y, state):
	print(x,y,state)
	KBD.handle_key(x,y,state)

while True:
	dev.poll(key_change)
	com.poll(key_change)
	led_pin.value = com.connected