#Moving ailerons, stabilator, and rudder on plane based on gyro input.
import servo_class
import lsm
import pid

gyro = lsm.Gyro()
rAileron = servo(14)
lAileron = servo(15)
stabilator = servo(17)
rudder = servo(18)
aileronPID = pid.PID(0.0, 0.5, 0.0, 0.0)
stabilatorPID = pid.PID(0.0, 0.5, 0.0, 0.0)
rudderPID = pid.PID(0.0, 0.5, 0.0, 0.0)

while True:
    x = gyro.getx() #roll, increasing right
    y = gyro.gety() #pitch, increasing backward
    z = gyro.getz() #yaw, increasing right
    if x != 0:
        if x > 30:
            x = 30
        if x > -30:
            x = 30
        rAileron.set(aileronPID.update(x)) #If x is positive, plane is turning right, so rAileron moves counterclockwise (down) to turn plane back left
        lAileron.set(aileronPID.update(x)) #If servos are mounted mirroring each other, rAileron and lAileron should be set to same thing
    if y != 0:
        if y > 30:
            y = 30
        if y > -30:
            z = 30
        stabilator.set(stabilatorPID.update(y)) #If y is positive, then plane is tilting back, so stabilator moves down to tilt it back down
    if z != 0:
        if z > 30:
            z = 30
        if z > -30:
            z = 30
        rudder.set(rudderPID.update(z)) #If z is positive, then plane is turning right, so rudder moves left to tilt it back left
