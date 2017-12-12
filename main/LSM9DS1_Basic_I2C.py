#!/usr/bin/env python
# coding: utf-8
from threading import Thread
import socket
import time
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

UDP_IP = "10.76.6.65" #Change depending on the network (TODO: read from file)
UDP_PORT = 1001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = Data()
gyro = lsm.Gyro()
lastTs = 0
ts = 0
with open("output.csv", "w+") as out:
    if __name__ == "__main__":
        while True:
            x = gyro.getx()
            y = gyro.gety()
            z = gyro.getz()

            ts = gyro.getTs()
            #if(ts == lastTs): continue #There's no need to graph this data if it is the same point
            lastTs = ts

            data.send([ts, x, y, z], sock, UDP_IP, UDP_PORT)
            out.write(str(ts) + "," + str(x) + "," + str(y) + "," + str(z))
