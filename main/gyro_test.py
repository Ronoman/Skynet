import lsm

gyro = lsm.Gyro()

while True:
    x = gyro.getx()
    y = gyro.gety()
    z = gyro.getGz()
    ts = gyro.getTs()

    print("dz: " + str(z) + "\t\tts: " + str(ts))
