from ctypes import *
import sys
import time
import math
from threading import Thread

class Gyro():
    def __init__(self):
        '''
        __init__ is automatically called when the Gyro object is constructed. It's
        purpose is to initialize the gyro library (lsm9ds1), and to instantiate
        the variables that we use later. We also begin communication with the
        gyro (imu), and start the thread that will read values from the board
        as quickly as possible.
        '''
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
        self.gy = 0
        self.gz = 0
        self.ts = time.time()*1000

        self.dx = [0]
        self.dy = [0]
        self.dz = [0]

        self.x = [0]
        self.y = [0]
        self.z = [0]

        self.ts = [time.time()*1000]

        updateThread = Thread(target=self.updateGyro, args=())
        updateThread.start()

    def gyroAvailable(self):
        '''
        gyroAvailable determines whether we can read another value from the gyro yet.
        '''
        return (self.lib.lsm9ds1_gyroAvailable(self.imu) == 1)

    def checkTolerance(self, a, b, c, tol):
        '''
        checkTolerance determines if values a, b, and c are all less than the
        provided tolerance. Not useful other than a helper function to updateGyro
        '''
        return (math.fabs(a)<tol and math.fabs(b)<tol and math.fabs(c)<tol)

    def updateGyro(self):
        '''
        updateGyro is where we get new values from our gyro, and calculate our new
        x, y, and z. Here is the sequence of events:

        1. Loop forever
        2. Wait until the gyro is ready for a read
        3. If the gyro values are not within the tolerance, skip this iteration
        4. Only save the last 10 read values
        5. Calculte the basic riemann sum

        We want this loop to run as fast as possible, to have the highest
        precision values we can.
        '''
        lastBad = False
        first = True
        while True:
            while not self.gyroAvailable():
                pass
            self.lib.lsm9ds1_readGyro(self.imu)
            self.gx = self.lib.lsm9ds1_getGyroX(self.imu) #gx, gy, gz are all raw gyro data
            self.gy = self.lib.lsm9ds1_getGyroY(self.imu)
            self.gz = self.lib.lsm9ds1_getGyroZ(self.imu)
            if(not first):
                if(self.checkTolerance(self.gx-self.dx[-1], self.gy-self.dy[-1], self.gz-self.dz[-1], 150) or lastBad):
                    self.dx.append(self.lib.lsm9ds1_calcGyro(self.imu, self.gx))
                    self.dy.append(self.lib.lsm9ds1_calcGyro(self.imu, self.gy))
                    self.dz.append(self.lib.lsm9ds1_calcGyro(self.imu, self.gz))
                    self.ts.append(time.time()*1000)
                    lastBad = False
                else:
                    lastBad = True
                    continue #Don't record the point if it is bad
            else:
                first = False
                continue #Can't do math if this is the first iteration of the loop

            self.dx = self.dx[-10:] #Keep the list of points fairly small
            self.dy = self.dy[-10:]
            self.dz = self.dz[-10:]
            self.ts = self.ts[-10:]

            self.x += [self.x[-1] + (self.dx[-1]*(self.ts[-1]-self.ts[-2])/1000)] #Do a simple riemann sum between the last point and this one
            self.x = self.x[-10:]
            self.y += [self.y[-1] + (self.dy[-1]*(self.ts[-1]-self.ts[-2])/1000)]
            self.y = self.y[-10:]
            self.z += [self.z[-1] + (self.dz[-1]*(self.ts[-1]-self.ts[-2])/1000)]
            self.z = self.z[-10:]

            #time.sleep(0.0001)

    def getx(self):
        '''
        The next 3 functions simply return the most recent gyro value for their
        respective axis.
        '''
        return self.x[-1]

    def gety(self):
        return self.y[-1]

    def getz(self):
        return self.z[-1]

    def getGz(self):
        '''
        getGz returns the most recent z axis speed, in deg/s
        '''
        try:
            return self.dz[-1]
        except IndexError:
            return 0

    def getTs(self):
        '''
        getTs returns the most recent timestamp, associated with the most recent
        gyro values.
        '''
        return self.ts[-1]
