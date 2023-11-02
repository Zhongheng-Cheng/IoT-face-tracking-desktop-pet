from machine import Pin, I2C
import ssd1306

class OLED(object):
    def __init__(self, pin_sda: int, pin_scl: int):
        i2c = I2C(sda=Pin(pin_sda), scl=Pin(pin_scl))
        self.display = ssd1306.SSD1306_I2C(128, 32, i2c)
        self.is_on = True
        return

    def show_text(self, content: list):
        '''
        Input:
            content: list[[text: str, x: int, y: int, 1], ]
        '''
        self.display.fill(0)
        if self.is_on:
            for i in content:
                self.display.text(i[0], i[1], i[2], i[3])
        self.display.show()
        return