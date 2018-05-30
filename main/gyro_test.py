import lsm

gyro = lsm.Gyro()

while True:
    x = gyro.getx()
    y = gyro.gety()
    z = gyro.getz()
    ts = gyro.getTs()

    print("x: " + str(x) + "\t\tts: " + str(ts))
