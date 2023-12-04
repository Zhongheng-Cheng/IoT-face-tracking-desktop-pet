from machine import ADC
from utime import sleep, time_ns
from socket import *
from uarray import array

class Microphone(object):
    def __init__(self):
        self.adc = ADC(0)
        return

    def record(self, seconds=5, depth=16, freq=8000):
        start_time = time_ns()
        data = array('h', [])
        print("start")
        for i in range(seconds):
            for j in range(freq):
                sample = self.adc.read() # adc.read() returns 10 bits
                data.append(sample)
            print(data)
            del data
            data = array('h', [])
        # for i in range(10):
        #     data.append(i)
        # print(data)
        check1 = time_ns() - start_time
        
        print("sample")
        print(seconds * freq / check1 * 1e9)
        return
