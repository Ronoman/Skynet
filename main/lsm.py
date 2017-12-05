from ctypes import *
import sys
import time
import math
from threading import Thread

class Gyro():
    def __init__(self):
        path = "../lib/liblsm9ds1cwrapper.so"
        self.lib = cdll.LoadLibrary(path)

        self.lib.lsm9ds1_create.argtypes = []
        self.lib.lsm9ds1_create.restype = c_void_p

        self.lib.lsm9ds1_begin.argtypes = [c_void_p]
        self.lib.lsm9ds1_begin.restype = None

        self.lib.lsm9ds1_calibrate.argtypes = [c_void_p]
        self.lib.lsm9ds1_calibrate.restype = None

        self.lib.lsm9ds1_gyroAvailable.argtypes = [c_void_p]
        self.lib.lsm9ds1_gyroAvailable.restype = c_int
        self.lib.lsm9ds1_accelAvailable.argtypes = [c_void_p]
        self.lib.lsm9ds1_accelAvailable.restype = c_int
        self.lib.lsm9ds1_magAvailable.argtypes = [c_void_p]
        self.lib.lsm9ds1_magAvailable.restype = c_int

        self.lib.lsm9ds1_readGyro.argtypes = [c_void_p]
        self.lib.lsm9ds1_readGyro.restype = c_int
        self.lib.lsm9ds1_readAccel.argtypes = [c_void_p]
        self.lib.lsm9ds1_readAccel.restype = c_int
        self.lib.lsm9ds1_readMag.argtypes = [c_void_p]
        self.lib.lsm9ds1_readMag.restype = c_int

        self.lib.lsm9ds1_getGyroX.argtypes = [c_void_p]
        self.lib.lsm9ds1_getGyroX.restype = c_float
        self.lib.lsm9ds1_getGyroY.argtypes = [c_void_p]
        self.lib.lsm9ds1_getGyroY.restype = c_float
        self.lib.lsm9ds1_getGyroZ.argtypes = [c_void_p]
        self.lib.lsm9ds1_getGyroZ.restype = c_float

        self.lib.lsm9ds1_getAccelX.argtypes = [c_void_p]
        self.lib.lsm9ds1_getAccelX.restype = c_float
        self.lib.lsm9ds1_getAccelY.argtypes = [c_void_p]
        self.lib.lsm9ds1_getAccelY.restype = c_float
        self.lib.lsm9ds1_getAccelZ.argtypes = [c_void_p]
        self.lib.lsm9ds1_getAccelZ.restype = c_float

        self.lib.lsm9ds1_getMagX.argtypes = [c_void_p]
        self.lib.lsm9ds1_getMagX.restype = c_float
        self.lib.lsm9ds1_getMagY.argtypes = [c_void_p]
        self.lib.lsm9ds1_getMagY.restype = c_float
        self.lib.lsm9ds1_getMagZ.argtypes = [c_void_p]
        self.lib.lsm9ds1_getMagZ.restype = c_float

        self.lib.lsm9ds1_calcGyro.argtypes = [c_void_p, c_float]
        self.lib.lsm9ds1_calcGyro.restype = c_float
        self.lib.lsm9ds1_calcAccel.argtypes = [c_void_p, c_float]
        self.lib.lsm9ds1_calcAccel.restype = c_float
        self.lib.lsm9ds1_calcMag.argtypes = [c_void_p, c_float]
        self.lib.lsm9ds1_calcMag.restype = c_float

        self.imu = self.lib.lsm9ds1_create()
        self.lib.lsm9ds1_begin(self.imu)
        if self.lib.lsm9ds1_begin(self.imu) == 0:
            print("Failed to communicate with LSM9DS1.")
            quit()
        self.lib.lsm9ds1_calibrate(self.imu)

        self.gx = 0
        self.cgx = 0
        self.gy = 0
        self.cgy = 0
        self.gz = 0
        self.cgz = 0
        self.ts = time.time()*1000

        self.dx = []
        self.dy = []
        self.dz = []

        self.x = [0]
        self.y = [0]
        self.z = [0]

        self.ts = [time.time()*1000]

        updateThread = Thread(target=self.updateGyro, args=())
        updateThread.start()

    def gyroAvailable(self):
        return (self.lib.lsm9ds1_gyroAvailable(self.imu) == 1)

    def updateGyro(self):
        lastBad = False
        first = True
        while True:
            while self.lib.lsm9ds1_gyroAvailable(self.imu) == 0:
                print("stuck")
                pass
            print("read")
            self.lib.lsm9ds1_readGyro(self.imu)
            self.gx = self.lib.lsm9ds1_getGyroX(self.imu)
            self.gy = self.lib.lsm9ds1_getGyroY(self.imu)
            self.gz = self.lib.lsm9ds1_getGyroZ(self.imu)
            if(not first):
                if(math.fabs(self.gx - self.dx[-1]) < 150 or lastBad):
                    if(math.fabs(self.gy - self.dy[-1]) < 150 or lastBad):
                        if(math.fabs(self.gz - self.dz[-1]) < 150 or lastBad):
                            self.dx.append(self.lib.lsm9ds1_calcGyro(self.imu, self.gx))
                            self.dy.append(self.lib.lsm9ds1_calcGyro(self.imu, self.gy))
                            self.dz.append(self.lib.lsm9ds1_calcGyro(self.imu, self.gz))
                            self.ts.append(time.time()*1000)
                            lastBad = False
                        else:
                            continue
                            lastBad = True
                    else:
                        continue
                        lastBad = True
                else:
                    continue
                    lastBad = True
            else:
                first = False
                continue

            self.dx = self.dx[-100:]
            self.dy = self.dy[-100:]
            self.dz = self.dz[-100:]
            self.ts = self.ts[-100:]

            self.x += [self.x[-1] + (self.dx[-1]*(self.ts[-1]-self.ts[-2])/1000)]
            self.x = self.x[-100:]
            self.y += [self.y[-1] + (self.dy[-1]*(self.ts[-1]-self.ts[-2])/1000)]
            self.y = self.y[-100:]
            self.z += [self.z[-1] + (self.dz[-1]*(self.ts[-1]-self.ts[-2])/1000)]
            self.z = self.z[-100:]

            time.sleep(0.001)

    def getx(self):
        return self.x[-1]

    def gety(self):
        return self.y[-1]

    def getz(self):
        return self.z[-1]

    def getGz(self):
        try:
            return self.dz[-1]
        except IndexError:
            return 0

    def getTs(self):
        return self.ts[-1]
