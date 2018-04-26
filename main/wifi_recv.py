import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 1001))

os.system("sudo pigpiod")

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
    message, address = sock.recvfrom(1024)
    message = message.decode("utf-8")

    if(float(message) < 0):
        pass

    val = translate(float(message), 0, 0.5, 1000, 2000)

    if(val < 1000):
        val = 1000
    if(val > 2000):
        val = 2000

    print("pigs s 12 " + str(val))
    #os.system("pigs s 12 " + str(translate(message, 0, 0.5, 1000, 2000)))
