from machine import Pin, PWM

class Servo(object):
    def __init__(self, 
                 pin: int, 
                 static_err: int = 0, 
                 degree_limit: list = [0, 180]
                 ):
        '''
        static_err: used for angle correction. 
            default: buttom_servo = -8; upper_servo = 0
        '''
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin, freq=50)
        self.static_err = static_err
        self.degree_limit = degree_limit
        self.degree = 90
        self.set_degree(self.degree)
        return
    
    def set_degree(self, degree: int):
        if degree < self.degree_limit[0]:
            degree = self.degree_limit[0]
        elif degree > self.degree_limit[1]:
            degree = self.degree_limit[1]
        self.degree = degree
        high_time = (self.degree + self.static_err) * 2 / 180 + 0.5
        duty = int(high_time / 20 * 1023)
        self.pwm.duty(duty)
        return
    
    