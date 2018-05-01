import socket
import time
import joystick
from threading import Thread
import pigpio
import lsm

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
        sock.sendto(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]), (ip, port))

def degToMs(degrees):
    ret = (degrees + 90.0)/(180.0) * (2000.0) + 500.0
    if(ret > 2500):
        ret = 2500
    elif(ret < 500):
        ret = 500
    return ret

UDP_IP = "10.76.6.34" #Change depending on the network (TODO: read from file)
UDP_PORT = 1001

SERVO_Z = 14
SERVO_Y = 15
SERVO_X = 18

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = Data()
gyro = lsm.Gyro()
lastTs = 0
ts = 0

max_x = 0
max_y = 0
max_z = 0

i = 0

pi = pigpio.pi()
pi.set_mode(SERVO_X, pigpio.OUTPUT)
pi.set_mode(SERVO_Y, pigpio.OUTPUT)
pi.set_mode(SERVO_Z, pigpio.OUTPUT)

UDP_IP = "10.76.0.100" #Change depending on the network (TODO: read from file)
UDP_PORT = 1001

joy = None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

joy = joystick.getFirstJoystick()
print(type(joy))

@joy.event
def on_axis(axis, value):
    print("axis: " +str(axis) + ", val: " + str(value))
    if(axis == "l_thumb_y" or axis == "r_thumb_x"):
        sock.sendto(axis + "," + str(value), (UDP_IP, UDP_PORT))

print("starting loop")
"""while True:
    joy.dispatch_events()
    time.sleep(0.01)"""

n = 1
with open("output.csv", "w+") as out:
    if __name__ == "__main__":
        while True:
            if(n % 5 == 0):
                x = gyro.getx()
                y = gyro.gety()
                z = gyro.getz()

                #print(z)

                pi.set_servo_pulsewidth(SERVO_Z, degToMs(-z))
                pi.set_servo_pulsewidth(SERVO_X, degToMs(-x))
                pi.set_servo_pulsewidth(SERVO_Y, degToMs(y))

                ts = gyro.getTs()
                #if(ts == lastTs): continue #There's no need to graph this data if it is the same point
                lastTs = ts

                data.send([ts, x, y, z], sock, UDP_IP, UDP_PORT)
                #out.write(str(ts) + "," + str(x) + "," + str(y) + "," + str(z))

            joy.dispatch_events()
            n = n + 1
            time.sleep(0.01)
