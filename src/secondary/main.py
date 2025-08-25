import board
import digitalio
import time

from common.kboard import K_Board
from common.klink import K_Link_Client

com = K_Link_Client(board.GP0, board.GP1)

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
	)
)

led_pin = digitalio.DigitalInOut(board.LED)
led_pin.switch_to_output()

while True:
	dev.poll(com.send_keydata)
	com.poll()
	led_pin.value = com.connected