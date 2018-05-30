#Moving ailerons, stabilator, and rudder on plane based on gyro input.
from servo_class import Servo
import lsm
import time
import pigpio
from pid import PID

pi = pigpio.pi()
gyro = lsm.Gyro()

rAileron = Servo(17)
lAileron = Servo(27)
rollPID = PID(0.0, -0.5, 0.0, 0.0)
stabilator = Servo(24)
stabilatorPID = PID(10.0, 1.0, 0.0, 0.0) #setpoint is 10 degrees for angle of attack
rudder = Servo(23)
rudderPID = PID(0.0, 0.5, 0.0, 0.0)

while True:
    x = gyro.getx() #roll, increasing right
    y = gyro.gety() #pitch, increasing backward
    z = gyro.getz() #yaw, increasing right

    print(z)
    """if y != 0:
        if y > 30:
            y = 30
        if y < -30:
            y = 30
        rAileron.set(rollPID.update(x)) #If y is positive, plane is turning left, so must turn plane back right
        lAileron.set(rollPID.update(x)) #If servos are mounted mirroring each other, rAileron and lAileron should be set to same thing
    if x != 0:
        if x > 30:
            x = 30
        if x < -30:
            x = 30
        stabilator.set(stabilatorPID.update(y)) #If x is positive, then plane is tilting back, so stabilator moves to tilt it back down
    if z != 0:
        if z > 30:
            z = 30
        if z < -30:
            z = 30
        rudder.set(rudderPID.update(z)) #If z is positive, then plane is turning right, so rudder moves left to tilt it back left"""
    if x != 0:
        n = rollPID.update(x)
        if n > 30:
            n = 30
        if n < -30:
            n = -30
        rAileron.set(n) #If x is positive, plane is turning left, so must turn plane back right
        lAileron.set(n) #If servos are mounted mirroring each other, rAileron and lAileron should be set to same thing
    if y != 0:
        n = stabilatorPID.update(y)
        if n > 30:
            n = 30
        if n < -30:
            n = -30
        stabilator.set(n) #If y is positive, then plane is tilting back, so stabilator moves to tilt it back down
    if z != 0:
        n = rudderPID.update(z)
        if n > 30:
            n = 30
        if n < -30:
            n = 30
        rudder.set(n) #If z is positive, then plane is turning right, so rudder moves left to tilt it back left
