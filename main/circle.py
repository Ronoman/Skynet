#Moving ailerons, stabilator, and rudder on plane based on gyro input.
from servo_class import servo
import lsm
import time
import pigpio
import pid

pi = pigpio.pi()
gyro = lsm.Gyro()
t = 0

rAileron = servo(18)
lAileron = servo(23)
rollPID = pid.PID(0.0, 0.5, 0.0, 0.0)
stabilator = servo(14)
stabilatorPID = pid.PID(10.0, 1.0, 0.0, 0.0) #setpoint is 10 degrees for angle of attack
rudder = servo(15)
rudderPID = pid.PID(0.0, 0.5, 0.0, 0.0)

while True:
    x = gyro.getx() #roll, increasing right
    y = gyro.gety() #pitch, increasing backward
    z = gyro.getz() #yaw, increasing right
    """if x != rollPID.setpoint:
        if x > 30:
            x = 30
        if x > -30:
            x = -30
        rAileron.set(rollPID.update(x)) #If x is positive, plane is turning right, so rAileron moves counterclockwise (down) to turn plane back left
        lAileron.set(rollPID.update(x)) #If servos are mounted mirroring each other, rAileron and lAileron should be set to same thing
    if y != 0:
        if y > 30:
            y = 30
        if y > -30:
            y = -30
        stabilator.set(stabilatorPID.update(y)) #If y is positive, then plane is tilting back, so stabilator moves down to tilt it back down
    if z != rudderPID.setpoint:
        if z > 30:
            z = 30
        if z > -30:
            z = -30
        rudder.set(rudderPID.update(z)) #If z is positive, then plane is turning right, so rudder moves left to tilt it back left"""
    if x != rollPID.setpoint:
        n = rollPID.update(x)
        if n > 30:
            n = 30
        if n > -30:
            n = -30
        rAileron.set(n) #If x is positive, plane is turning right, so rAileron moves counterclockwise (down) to turn plane back left
        lAileron.set(n) #If servos are mounted mirroring each other, rAileron and lAileron should be set to same thing
    if y != 0:
        n = stabilatorPID.update(y)
        if n > 30:
            n = 30
        if n > -30:
            n = -30
        stabilator.set(n) #If y is positive, then plane is tilting back, so stabilator moves down to tilt it back down
    if z != rudderPID.setpoint:
        n = rudderPID.update(z)
        if n > 30:
            n = 30
        if n > -30:
            n = -30
        rudder.set(n) #If z is positive, then plane is turning right, so rudder moves left to tilt it back left
    rollPID.set_setpoint(t*(360/30))
    rollPID.set_setpoint(t*(360/30))
    rudder.set_setpoint(t*(360/30))
