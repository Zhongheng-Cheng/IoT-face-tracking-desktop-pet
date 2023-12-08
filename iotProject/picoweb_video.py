# This section uses firmware from Lemariva's Micropython-camera-driver.  
# for details, please refer to: https://github.com/lemariva/micropython-camera-driver  
import picoweb
import utime
import gc
import socket
import camera
import machine
import time


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
            #print("connect timeout!")
            break
#     if wlan.isconnected():
        #print('network connected!, network config:', wlan.ifconfig())

# Initializing the Camera
def camera_init():
    # Disable camera initialization
    camera.deinit()
    # Enable camera initialization
    camera.init(0, d0=4, d1=5, d2=18, d3=19, d4=36, d5=39, d6=34, d7=35,
                format=camera.JPEG, framesize=camera.FRAME_240X240, 
                xclk_freq=camera.XCLK_20MHz,
                href=23, vsync=25, reset=-1, pwdn=-1,
                sioc=27, siod=26, xclk=21, pclk=22, fb_location=camera.PSRAM)
# 初始化摄像头
    #camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)

    camera.framesize(camera.FRAME_240X240) # Set the camera resolution
    # The options are the following:
    # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
    # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
    # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA
    # Note: The higher the resolution, the more memory is used.
    # Note: And too much memory may cause the program to fail.
#     
#   camera.flip(1)                       # Flip up and down window: 0-1
    camera.mirror(0)                     # Flip window left and right: 0-1
#     camera.saturation(0)                 # saturation: -2,2 (default 0). -2 grayscale 
#     camera.brightness(0)                 # brightness: -2,2 (default 0). 2 brightness
#     camera.contrast(0)                   # contrast: -2,2 (default 0). 2 highcontrast
    camera.quality(30)                   # quality: # 10-63 lower number means higher quality
    # Note: The smaller the number, the sharper the image. The larger the number, the more blurry the image
    
    camera.speffect(camera.EFFECT_NONE)  # special effects:
    # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO
    camera.whitebalance(camera.WB_NONE)  # white balance
    # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

# Send camera pictures
def send_frame(s):
    buf = camera.capture()
    s.sendto(buf, ('34.135.180.148', 8011))
    print('send image')
    print(buf)

    del buf
    gc.collect()
    
def send_frametocomputer():
    
    buf = camera.capture()
    #print('send image')
    print(buf)
    del buf
    gc.collect()

if __name__ == '__main__':
    
    #uart = machine.UART(1, baudrate=115200)  # UART1, 115200波特率
#     uart.init(4800, bits=8, parity=None, stop=1)  # 初始化UART设置
#     import ulogging as logging
#     logging.basicConfig(level=logging.INFO)
    camera_init()
    wifi_connect()
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    while True:
        #send_frame(s)
        send_frametocomputer()
        utime.sleep(1)


