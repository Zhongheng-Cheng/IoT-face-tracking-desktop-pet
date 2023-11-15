from machine import Pin, I2C, SPI
import ssd1306
from time import sleep_ms

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

class LCD_2inch(object):
    def __init__(self, CS_PIN, DC_PIN, RST_PIN=None, BL_PIN=None):
        '''
        ESP8266 - LCD 2inch module
        GPIO 12 (MISO) - None
        GPIO 13 (MOSI) - DIN
        GPIO 14 (SCK) - CLK
        '''
        self.spi = SPI(1, baudrate=40000000, polarity=1, phase=1)
        self.cs = Pin(CS_PIN, Pin.OUT)
        self.dc = Pin(DC_PIN, Pin.OUT)
        self.rst = Pin(RST_PIN, Pin.OUT)
        self.bl = Pin(BL_PIN, Pin.OUT)
        self.width = 240
        self.height = 320
        return

    def write_command(self, command: int):
        self.dc.value(0)
        self.spi.write(chr(command).encode())
        return

    def write_data(self, data):
        self.dc.value(1)
        if type(data) == int:
            self.spi.write(chr(data).encode())
        elif type(data) == list:
            for i in data:
                self.spi.write(chr(i).encode())
        return
    
    def reset(self):
        if self.rst:
            self.rst.value(1)
            sleep_ms(10)
            self.rst.value(0)
            sleep_ms(10)
            self.rst.value(1)
            sleep_ms(10)
        return

    def init(self):
        self.reset()

        # 设置显示屏的扫描方向
        self.write_command(0x36) 
        self.write_data(0x00) 

        # 设置像素格式
        self.write_command(0x3A) 
        self.write_data(0x05)

        # 启用扩展命令集
        self.write_command(0x21) 

        # 设置 X 轴的窗口位置
        self.write_command(0x2A) 
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3F)

        # 设置 Y 轴的窗口位置
        self.write_command(0x2B) 
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        # 可能涉及到电源管理和其他控制
        self.write_command(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_command(0xB7)
        self.write_data(0x35) 

        self.write_command(0xBB)
        self.write_data(0x1F)

        self.write_command(0xC0)
        self.write_data(0x2C)

        self.write_command(0xC2)
        self.write_data(0x01)
                        
        self.write_command(0xC3)
        self.write_data(0x12)   

        self.write_command(0xC4)
        self.write_data(0x20)

        self.write_command(0xC6)
        self.write_data(0x0F) 

        self.write_command(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        # 可能是设置 Gamma 校正，用于调整显示颜色的亮度和对比度
        self.write_command(0xE0) 
        self.write_data(0xD0)
        self.write_data(0x08)
        self.write_data(0x11)
        self.write_data(0x08)
        self.write_data(0x0C)
        self.write_data(0x15)
        self.write_data(0x39)
        self.write_data(0x33)
        self.write_data(0x50)
        self.write_data(0x36)
        self.write_data(0x13)
        self.write_data(0x14)
        self.write_data(0x29)
        self.write_data(0x2D)

        self.write_command(0xE1)
        self.write_data(0xD0)
        self.write_data(0x08)
        self.write_data(0x10)
        self.write_data(0x08)
        self.write_data(0x06)
        self.write_data(0x06)
        self.write_data(0x39)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x0B)
        self.write_data(0x16)
        self.write_data(0x14)
        self.write_data(0x2F)
        self.write_data(0x31)

        # 可能是禁用扩展命令集
        self.write_command(0x21) 

        # 退出睡眠状态
        self.write_command(0x11) 

        # 启动显示
        self.write_command(0x29) 
        return
    
    def set_window(self, x_start, y_start, x_end, y_end):
        self.write_command(0x2A) # Set the x coordinates
        self.write_data(x_start >> 8) # 发送 X 起始坐标的高8位
        self.write_data(x_start & 0xff) # 发送 X 起始坐标的低8位
        self.write_data(x_end >> 8) # 发送 X 结束坐标的高8位
        self.write_data((x_end - 1) & 0xff) # 发送 X 结束坐标的低8位，减去1是因为坐标通常是从0开始计数

        self.write_command(0x2B) # Set the y coordinates
        self.write_data(y_start >> 8) # 发送 Y 起始坐标的高8位
        self.write_data(y_start & 0xff) # 发送 Y 起始坐标的低8位
        self.write_data(y_end >> 8)# 发送 Y 结束坐标的高8位
        self.write_data((y_end - 1) & 0xff) # 发送 Y 结束坐标的低8位

        self.write_command(0x2C) # 开始写入像素数据
        
    def clear(self):
        buffer = [0xff] * (self.width * self.height * 2)
        self.set_window(0, 0, self.height, self.width)
        for i in range(0, len(buffer), 4096):
            self.write_data(buffer[i:i + 4096])
        return