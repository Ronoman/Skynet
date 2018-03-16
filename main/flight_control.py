#Moving ailerons, stabilator, and rudder on plane based on gyro input.
from servo_class import servo
import lsm
import time
import pigpio

pi = pigpio.pi()
gyro = lsm.Gyro()

rAileron = servo(18)
lAileron = servo(23)
stabilator = servo(14)
rudder = servo(15)

while True:
    x = gyro.getx() #roll, increasing right
    y = gyro.gety() #pitch, increasing backward
    z = gyro.getz() #yaw, increasing right
    if x != 0:
        if x > 30:
            x = 30
        if x > -30:
            x = 30
        rAileron.set(-x) #If x is positive, plane is turning right, so rAileron moves counterclockwise (down) to turn plane back left
        lAileron.set(-x) #If servos are mounted mirroring each other, rAileron and lAileron should be set to same thing
    if y != 0:
        if y > 30:
            y = 30
        if y > -30:
            y = 30
        stabilator.set(-y) #If y is positive, then plane is tilting back, so stabilator moves down to tilt it back down
    if z != 0:
        if z > 30:
            z = 30
        if z > -30:
            z = 30
        rudder.set(-z) #If z is positive, then plane is turning right, so rudder moves left to tilt it back left
