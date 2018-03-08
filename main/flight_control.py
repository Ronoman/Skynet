#Moving ailerons, stabilator, and rudder on plane based on gyro input.
import servo_class
import lsm

gyro = lsm.Gyro()
rAileron = servo_class(14)
lAileron = servo_class(15)
stabilator = servo_class(17)
rudder = servo_class(18)

while True:
    x = gyro.getx() #roll, increasing right
    y = gyro.gety() #pitch, increasing backward
    z = gyro.getz() #yaw, increasing right
    if x != 0:
        #fixt that
    if y != 0:
        #fix that
    if z != 0:
        #fix that
