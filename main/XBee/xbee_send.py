import serial
import time
from xbee import XBee

serial_port = serial.Serial('/dev/ttyUSB0', 9600)

def print_data(data):
    print data

xbee = XBee(serial_port, callback=print_data)

while True:
    try:
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

xbee.halt()
serial_port.close()
