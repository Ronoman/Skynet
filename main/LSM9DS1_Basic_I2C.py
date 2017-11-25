#!/usr/bin/env python
# coding: utf-8
import lsm
import time
import socket
from threading import Thread

class Data():
    def __init__(self):
        self.dx = [0, 0]
        self.dy = [0, 0]
        self.dz = [0, 0]

        self.x = [0, 0]
        self.y = [0, 0]
        self.z = [0, 0]

        self.ts = []

    def update(self, dx, dy, dz, ts):
        self.dx += [dx]
        self.dx = self.dx[-100:]
        self.dy += [dy]
        self.dy = self.dy[-100:]
        self.dz += [dz]
        self.dz = self.dz[-100:]

        self.ts += [ts]
        self.ts = self.ts[-100:]

        self.x += [self.x[-1] + (self.dx[-1]*(self.x[-1]-self.x[-2])/1000)]
        self.x = self.x[-100:]
        self.y += [self.y[-1] + (self.dy[-1]*(self.y[-1]-self.y[-2])/1000)]
        self.y = self.y[-100:]
        self.z += [self.z[-1] + (self.dz[-1]*(self.z[-1]-self.z[-2])/1000)]
        self.z = self.z[-100:]

        # print("timestamp: ",[self.ts[-1]])
        # print("x: ",self.x[-1])
        # print("y: ",self.y[-1])
        # print("z: ",self.z[-1])

    def send(self, sock, ip, port):
        while True:
            sock.sendto(str(self.ts[-1]) + "," + str(self.x[-1]) + "," + str(self.y[-1]) + "," + str(self.z[-1]))
            time.sleep(0.05)

UDP_IP = "10.0.0.242" #Change depending on the network (TODO: read from file)
UDP_PORT = 1001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = Data()
gyro = lsm.Gyro()
with open("output.csv", "w+") as out:
    if __name__ == "__main__":
        while True:
            while not gyro.gyroAvailable():
                pass

            gx = gyro.getGx()
            gy = gyro.getGy()
            gz = gyro.getGz()

            data.update(time.time()*1000, gx, gy, gz, UDP_IP, UDP_PORT)
            data.send(sock)
            out.write(str(time.time()*1000) + "," + str(gx) + "," + str(gy) + "," + str(gz))
