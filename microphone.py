from machine import ADC
from utime import sleep
from socket import *
# import gc

SERVER_NAME = "192.168.1.158"
SERVER_PORT = int(input("SERVER_PORT: "))

class Microphone(object):
    def __init__(self):
        self.adc = ADC(0)
        self.serverConnection()
        return
    
    def record(self, seconds=5, depth=16, freq=8000):
        for i in range(seconds):
            # wave_data = ''
            wave_data = bytearray()

            for j in range(freq):
                sample = self.adc.read() # adc.read() returns 10 bits
                high_8bits = sample >> 2
                high_8bits = high_8bits | 0xf0
                low_8bits = sample & 0xff
                wave_data.append(high_8bits)
                wave_data.append(low_8bits)
                sleep(1 / freq)
            self.clientSocket.sendall(wave_data)
            # print(self.wave_data)
            print("=========================")
            
            # del wave_data
            # wave_data = ''
            # gc.collect()
        self.clientSocket.send(b'\n')
        return



    def serverConnection(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((SERVER_NAME, SERVER_PORT))
        print("Successfully connected")
        return