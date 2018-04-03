#Servo class definition
from threading import Thread
import socket
import pigpio
import time

pi = pigpio.pi()

class servo():
    def __init__(self, port):
        self.port = port
        pi.set_mode(port, pigpio.OUTPUT)
    def degToMs(self, degrees):
        ret = (degrees + 90.0)/(180.0) * (2000.0) + 500.0
        if(ret > 2500):
            ret = 2500
        elif(ret < 500):
            ret = 500
        return ret
    def set(self, degrees):
        pi.set_servo_pulsewidth(self.port, self.degToMs(degrees))
