from threading import Thread
import socket
import pigpio
import time
from servo_class import servo

pi = pigpio.pi()
pi.set_mode(23, pigpio.OUTPUT)

myServo = servo(14)

def degToMs(degrees):
	ret = (degrees + 90.0)/(180.0) * (2000.0) + 500.0
	if(ret>2500):
		ret = 2500
	elif(ret < 500):
		ret = 500
	return ret

def set(degrees):
	pi.set_servo_pulsewidth(23, degToMs(degrees))

myServo.set(15)
set(15)
