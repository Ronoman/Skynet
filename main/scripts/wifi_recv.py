import socket
import pigpio
import sys
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001))

SERVO_LEFT = 17
SERVO_RIGHT = 27
SERVO_ELEVATOR = 24
SERVO_MIN = 500
SERVO_MAX = 2500

os.system("sudo pigpiod")

pi = pigpio.pi()
pi.set_mode(SERVO_LEFT, pigpio.OUTPUT)
pi.set_mode(SERVO_RIGHT, pigpio.OUTPUT)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

while True:
    # i += 1
    print("Recv'd")
    message, address = sock.recvfrom(1024)
    message = message.decode("utf-8")
    if(message == "kill"):
        os.system("pigs s 12 1000")
        sys.exit()
    message = message.split(",")

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
        os.system("pigs s 12 " + str(translate(float(message[1]), 0, 0.5, 1000, 2000)))

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
