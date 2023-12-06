from networks import NetworkConn
from servo import Servo

SERVER_IP = "34.135.180.148"
SERVER_PORT = int(input("server port: "))

def trace_center(center_x, center_y, threshold=0):
    if center_x != 0 or center_y != 0:
        delta_degree_x = delta_loc_to_degree(center_x - 120, threshold)
        delta_degree_y = delta_loc_to_degree(center_y - 120, threshold)
        return -delta_degree_x, -delta_degree_y
    return None

def delta_loc_to_degree(delta_loc, threshold=0):
    '''
    -120 <= delta_loc <= 120
    -30 <= delta_degree <= 30
    '''
    if -120 <= delta_loc <= -threshold:
        delta_degree = int((delta_loc + threshold) / 4)

    elif -threshold <= delta_loc <= threshold:
        delta_degree = 0

    elif threshold <= delta_loc <= 120:
        delta_degree = int((delta_loc - threshold) / 4)

    return delta_degree


if __name__ == '__main__':
    network_conn = NetworkConn()
    network_conn.connect_to_server(SERVER_IP, SERVER_PORT)

    buttom_servo = Servo(pin=12, static_err=-8)
    upper_servo = Servo(pin=14, degree_limit=[90, 180])

    while True:
        center = network_conn.clientSocket.recv(2)
        center_x = int(center[0])
        center_y = int(center[1])
        print(f"location: ({center_x}, {center_y})")
        trace_result = trace_center(center_x, center_y, threshold=30)
        if trace_result:
            delta_degree_x, delta_degree_y = trace_result
            print(f'delta_degree: ({delta_degree_x}, {delta_degree_y})')
            print()
            buttom_servo.set_delta_degree(delta_degree_x)
            upper_servo.set_delta_degree(delta_degree_y)




    # =================== Infrared Sensor

    # from sensors import InfraredSensor
    # from utime import sleep
    # infra = InfraredSensor(14)
    # while True:
    #     sleep(0.1)
    #     print(infra.read())


    # ############### Microphone

    # from microphone import Microphone

    # mic = Microphone()
    # mic.record(seconds=5)


# import random
# from machine import Pin,SPI
# import st7789py as st7789
 
# def main():
#     spi = SPI(1,baudrate = 80_000_000,polarity = 1,sck = Pin(2),mosi = Pin(3),miso = None)
#     tft = st7789.ST7789(spi,240,240,reset = Pin(0,Pin.OUT),dc = Pin(2,Pin.OUT),cs = None,backlight = None,rotation = 0)#rotation 方向0-4方位
 
#     tft.fill(st7789.BLACK)
 
#     while True:
#         tft.line(
#             random.randint(0, tft.width),
#             random.randint(0, tft.height),
#             random.randint(0, tft.width),
#             random.randint(0, tft.height),
#             st7789.color565(
#                 random.getrandbits(8),
#                 random.getrandbits(8),
#                 random.getrandbits(8)
#                 )
#             )
 
#         width = random.randint(0, tft.width // 2)
#         height = random.randint(0, tft.height // 2)
#         col = random.randint(0, tft.width - width)
#         row = random.randint(0, tft.height - height)
#         tft.fill_rect(
#             col,
#             row,
#             width,
#             height,
#             st7789.color565(
#                 random.getrandbits(8),
#                 random.getrandbits(8),
#                 random.getrandbits(8)
#             )
#         )
 
# if __name__ == "__main__":
#     main()