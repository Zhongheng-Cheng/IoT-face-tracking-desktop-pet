from machine import ADC
from utime import sleep
from socket import *
import gc

SERVER_NAME = "192.168.1.158"
SERVER_PORT = 8011

class Microphone(object):
    def __init__(self):
        self.adc = ADC(0)
        self.serverConnection()
        return
    
    def record(self, seconds=5, depth=16, freq=8000):
        for _ in range(seconds):
            self.wave_data = ''

            # send data every half-second
            for i in range(seconds * 8):
                for j in range(freq / 8):
                    sample = self.adc.read() * 2 ** (depth - 10) # adc.read() returns 10 bits
                    self.wave_data += str(sample) + ' '
                    sleep(1 / freq)
                self.clientSocket.send(self.wave_data.encode())
                # print(self.wave_data)
                print("=========================")
                self.wave_data = ''
                gc.collect()
        return

    def serverConnection(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((SERVER_NAME, SERVER_PORT))
        print("Successfully connected")
        return