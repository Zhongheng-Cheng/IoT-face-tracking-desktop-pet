import ssd1306
from machine import Pin, SoftI2C
from socket import *
import utime
class OLED(object):
    def __init__(self, pin_sda: int, pin_scl: int):
        i2c = SoftI2C(sda=Pin(pin_sda), scl=Pin(pin_scl))
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
    
    def show_emotion(self, mood):
        def draw_large_eye(x, y):
            for dy in range(-1, 2):
                for dx in range(-2, 3):
                    self.display.pixel(x+dx, y+dy, 1)

        def draw_large_mouth(x, y, mood):

            if mood == "Happy":

                self.display.line(x-6, y, x-3, y+3, 1)
                self.display.line(x-3, y+3, x+3, y+3, 1)
                self.display.line(x+3, y+3, x+6, y, 1)
            elif mood == "Sad":

                self.display.line(x-6, y+3, x-3, y, 1)
                self.display.line(x-3, y, x+3, y, 1)
                self.display.line(x+3, y, x+6, y+3, 1)
            else:
                self.display.line(x-4, y, x+4, y, 1)


        self.display.fill(0)
        eye_x = 44
        eye_y = 8
        draw_large_eye(eye_x, eye_y)
        draw_large_eye(eye_x + 40, eye_y)

        mouth_x = 64
        mouth_y = 20
        draw_large_mouth(mouth_x, mouth_y, mood)

        self.display.show()


#SSID = "Verizon_74NQTL"
#PASSWORD = "month3-hold-hut"    # Enter your WiFi password
SSID = "Columbia University"         # Enter your WiFi name
PASSWORD = ""    # Enter your WiFi password

# Let ESP32 connect to wifi.
def wifi_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        #print('connecting to network...')
        wlan.connect(SSID, PASSWORD) 
    start = utime.time()
    while not wlan.isconnected():
        utime.sleep(1)
        if utime.time()-start > 10:
            print("connect timeout!")
            break
if __name__ == '__main__':
    wifi_connect()
    print('wifi connected')
    serverIp = '35.188.219.151'
    port = 8013
    screen = OLED(pin_sda=21, pin_scl=22)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((serverIp, port))
    while True:
        emotion = client_socket.recv(1024).decode()
        print(emotion)
        screen.show_emotion(emotion)