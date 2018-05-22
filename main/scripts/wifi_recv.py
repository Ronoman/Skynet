from threading import Thread
import socket
import serial
import pigpio
import time
import sys
import lsm
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001)) #For receiving command data

xbee = serial.Serial('/dev/ttyS0', 9600, timeout=0.001)

UDP_IP = 0
UDP_PORT = 0

SERVO_LEFT = 17
SERVO_RIGHT = 27
SERVO_ELEVATOR = 24
SERVO_MIN = 500
SERVO_MAX = 2500

os.system("sudo pigpiod")

pi = pigpio.pi()
# pi.set_mode(SERVO_LEFT, pigpio.OUTPUT)
# pi.set_mode(SERVO_RIGHT, pigpio.OUTPUT)
# os.system("pigs s 12 1000")

class Data():
    def __init__(self):
        self.dx = []
        self.dy = []
        self.dz = []

        self.x = [0]
        self.y = [0]
        self.z = [0]

        self.ts = [time.time()*1000]

    def send(self, data, sock, ip, port):
        #WiFi
        #sock.sendto(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]), (ip, port))

        #XBee
        xbee.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]))

data = Data()
gyro = lsm.Gyro()
lastTs = 0
ts = 0

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def controlReceiver():
    while True:
        #message, address = sock.recvfrom(1024)
        #message = message.decode("utf-8")
        message = xbee.readline()
        if(message == "kill"):
            #os.system("pigs s 12 1000")
            sys.exit()
        message = message.split(",")
        if(message[0] == ""):
            continue

        print(message[0])

        if(message[0] == "l_thumb_y"):
            if(float(message[1]) < 0):
                pass
            val = translate(float(message[1]), 0, 1, 1000, 2000)

            if(val < 1000):
                val = 1000
            if(val > 2000):
                val = 2000

            #print("pigs s 12 " + str(val))
            #os.system("pigs s 12 " + str(translate(float(message[1]), 0, 0.5, 1000, 2000)))

        elif(message[0] == "r_thumb_x"):
            val = translate(float(message[1]), -0.5, 0.5, SERVO_MIN, SERVO_MAX)

            if(val < 500):
                val = 500
            if(val > 2500):
                val = 2500

            print(val)

            pi.set_servo_pulsewidth(SERVO_LEFT, val)
            pi.set_servo_pulsewidth(SERVO_RIGHT, val)
        elif(message[0] == "r_thumb_y"):
            val = translate(float(message[1]), -0.5, 0.5, SERVO_MIN, SERVO_MAX)

            if(val < 500):
                val = 500
            if(val > 2500):
                val = 2500

            pi.set_servo_pulsewidth(SERVO_ELEVATOR, val)

def gyroSender():
    while True:
        x = gyro.getx()
        y = gyro.gety()
        z = gyro.getz()

        #print(z)

        #pi.set_servo_pulsewidth(SERVO_Z, degToMs(-z))
        #pi.set_servo_pulsewidth(SERVO_X, degToMs(-x))
        #pi.set_servo_pulsewidth(SERVO_Y, degToMs(y))

        ts = gyro.getTs()
        #if(ts == lastTs): continue #There's no need to graph this data if it is the same point
        lastTs = ts

        data.send([ts, x, y, z], sock, UDP_IP, UDP_PORT)

if __name__ == "__main__":
    print("Name is in fact main")
    receiverThread = Thread(target=controlReceiver, args=())
    receiverThread.daemon = True

    senderThread = Thread(target=gyroSender, args=())
    senderThread.daemon = True

    receiverThread.start()
    senderThread.start()

    while True:
        time.sleep(1)
