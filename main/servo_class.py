#Servo class definition
class servo():
    def __init__(self, port):
        self.port = port
        pi = pigpio.pi()
        pi.set_mode(port, pigpio.OUTPUT)
    def degToMs(degrees):
        ret = (degrees + 90.0)/(180.0) * (2000.0) + 500.0
        if(ret > 2500):
            ret = 2500
        elif(ret < 500):
            ret = 500
        return ret
    def set(degrees):
        pi.set_servo_pulsewidth(self.port, degToMs(degrees))
