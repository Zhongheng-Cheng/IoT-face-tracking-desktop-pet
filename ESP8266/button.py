from machine import Pin
from time import sleep_ms, time

class Button:
    def __init__(self, pin: int, press=None, release=None, long_press=None):
        self.pin = pin
        self.press_func = press
        self.release_func = release
        self.long_press_func = long_press
        self.count = 0
        self.state = 1 # not pressed
        self.press_time = 0

        p = Pin(self.pin, Pin.IN)
        p.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._callback)
        return

    def _callback(self, p: int):
        sleep_ms(10)
        if p.value() != self.state:
            self.state = p.value()
            self.count += 1
            if self.state == 1:
                if self.long_press_func and time() - self.press_time >= 2:
                    self.long_press_func(p)
                    self.press_time = 0
                elif self.release_func:
                    self.release_func(p)
                # print("Button released", self.count)
            else:
                if self.press_func:
                    self.press_func(p)
                elif self.long_press_func:
                    self.press_time = time()
                # print("Button pressed", self.count)
        return