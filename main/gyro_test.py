import lsm

gyro = lsm.Gyro()

while True:
    x = gyro.getGx()
    y = gyro.getGy()
    z = gyro.getGz()
    ts = gyro.getTs()

    print("dx: " + str(x) + "\t\tts: " + str(ts))
