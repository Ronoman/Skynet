#Playing with servos
from threading import Thread
import socket
import pigpio
import time

def degToMs(degrees):
    ret = (degrees + 90.0)/(180.0) * (2000.0) + 500.0
    if(ret > 2500):
        ret = 2500
    elif(ret < 500):
        ret = 500
    return ret

SERVO_PORT1 = 17
SERVO_PORT2 = 27
SERVO_PORT3 = 24
SERVO_PORT4 = 18

pi = pigpio.pi()
pi.set_mode(SERVO_PORT1, pigpio.OUTPUT)
pi.set_mode(SERVO_PORT2, pigpio.OUTPUT)
pi.set_mode(SERVO_PORT3, pigpio.OUTPUT)
pi.set_mode(SERVO_PORT4, pigpio.OUTPUT)

while True:
    deg = float(raw_input("Deg: "))
    print(degToMs(deg))
    pi.set_servo_pulsewidth(SERVO_PORT1, degToMs(deg))
    pi.set_servo_pulsewidth(SERVO_PORT2, degToMs(deg))
    pi.set_servo_pulsewidth(SERVO_PORT3, degToMs(deg))
    pi.set_servo_pulsewidth(SERVO_PORT4, degToMs(deg))
