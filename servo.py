from machine import Pin, PWM

class Servo(object):
    def __init__(self, 
                 pin: int, 
                 static_err: int = None
                 ):
        '''
        static_err: used for angle correction. 
            default: buttom_servo = -8; upper_servo = 0
        '''
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin, freq=50)
        if static_err:
            self.static_err = static_err
        else:
            self.static_err = 0
        return
    
    def set_pwm(self, degree: int):
        assert degree >= 0 and degree <= 180
        high_time = (degree + self.static_err) * 2 / 180 + 0.5
        duty = int(high_time / 20 * 1023)
        self.pwm.duty(duty)
        return