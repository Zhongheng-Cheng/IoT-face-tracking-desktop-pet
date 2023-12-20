from machine import Pin, SPI, ADC

class LightSensor(object):
    def __init__(self, adc: int):
        # analog pin init
        self.adc = ADC(adc)  # read from 0 to 1024
        return

    def check_light_value(self):
        '''
        Output:
            self.light_value: int, ranging from 0 to 255
        '''
        self.light_value = int(self.adc.read() - 1) // 4
        return


class Accelerometer(object):
    def __init__(self):
        '''
        ESP8266 - ADXL345
        GPIO 12 (MISO) - SDO
        GPIO 13 (MOSI) - SDA
        GPIO 14 (SCK) - SCL
        GPIO 15 (Output) - CS
        '''
        self.spi = SPI(1, baudrate=2000000, polarity=1, phase=1)
        self.cs = Pin(15, Pin.OUT)
        self._meter_config(
            BW_RATE = b'\x2c\x0A',
            POWER_CTL = b'\x2d\x08',
            INT_ENABLE = b'\x2e\x00',
            DATA_FORMAT = b'\x31\x08',
            FIFO_CTL = b'\x38\x00'
        )
        self.reg_data_list = [0] * 6
        self.axis_accel = [0] * 3
        return

    def read_data(self):
        '''
        Read data from registers. 
        Order: x1, x2, y1, y2, z1, z2
        Output:
            axis_accel: [x_accel, y_accel, z_accel]
        '''
        for reg_index in range(6):
            reg = 0xf2 + reg_index
            self.reg_data_list[reg_index] = self._read_reg(reg)[1]
        for i in range(3):
            self.axis_accel[i] = self._get_accel(self.reg_data_list[i * 2], self.reg_data_list[i * 2 + 1])
        return self.axis_accel
    
    def _read_reg(self, reg):
        self.cs.value(0)
        reg_data = self.spi.read(2, reg)
        self.cs.value(1)
        return reg_data
    
    def _meter_config(self, BW_RATE, POWER_CTL, INT_ENABLE, DATA_FORMAT, FIFO_CTL):
        self.cs.value(0)
        self.spi.write(BW_RATE)
        self.spi.write(POWER_CTL)
        self.spi.write(INT_ENABLE)
        self.spi.write(DATA_FORMAT)
        self.spi.write(FIFO_CTL)
        self.cs.value(1)
        return
    
    def _get_accel(self, num1, num2):
        num = num2 << 8 | num1
        if num > 32767:
            num -= 65536
        return num

class InfraredSensor(object):
    def __init__(self, pin: int):
        self.pin = Pin(pin, Pin.IN)
        return
    
    def is_detect(self):
        if self.pin.value() == 0:
            return True
        else:
            return False
