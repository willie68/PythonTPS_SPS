import board
import digitalio
import time
import usb_cdc

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
serial = usb_cdc.data

while True:
    serial.write(bytearray("Hello, CircuitPython!"))
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)