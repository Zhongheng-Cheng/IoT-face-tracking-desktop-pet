from machine import Pin, PWM

class Servo(object):
    def __init__(self, pin: int):
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin, freq=50)
        self.static_err = -8 # for the buttom servo, the static degree error is -8 degree.
        return
    
    def set_pwm(self, degree: int):
        assert degree >= 0 and degree <= 180
        high_time = (degree + self.static_err) * 2 / 180 + 0.5
        print(f"degree = {degree}")
        print(f"high_time = {high_time}")
        duty = int(high_time / 20 * 1023)
        self.pwm.duty(duty)
        return



