import lsm

gyro = lsm.Gyro()

while True:
    x = gyro.getGx()
    y = gyro.gety()
    z = gyro.getz()
    ts = gyro.getTs()

    print("dx: " + str(x) + "\t\tts: " + str(ts))
