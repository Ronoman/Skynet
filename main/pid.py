# PID Class definition
class PID():
    def __init__(self, setpoint, kp, ki, kd):
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0.0
        self.last_error = 0.0
        self.integral = 0.0
    def set_setpoint(self, new_setpoint):
        #For changing set point
        self.setpoint = new_setpoint
    def set_kp(self, new_kp):
        #For changing kp
        self.kp = new_kp
    def ki(self, new_ki):
        #For changing ki
        self.ki = new_ki
    def kd(self, new_kd):
        #For changing kd
        self.kd = new_kd
    def update(self, sens_val):
        #Find error
        self.error = sens_val - self.setpoint
        #P Value
        P = self.kp * self.error
        #I Value
        self.integral = self.integral + self.error
        I = self.ki * self.integral
        #D Value
        D = self.kd * (self.error - self.last_error)
        self.last_error = self.error
        #Final Output
        return P + I + D
