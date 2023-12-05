from networks import NetworkConn
from servo import Servo

SERVER_IP = "34.41.9.51"
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

    buttom_servo = Servo(pin=14, static_err=-8)
    upper_servo = Servo(pin=12, degree_limit=[90, 180])

    while True:
        center = network_conn.clientSocket.recv(2)
        center_x = int(center[0])
        center_y = int(center[1])
        # center_x = int(input("center_x: "))
        # center_y = int(input("center_y: "))
        trace_result = trace_center(center_x, center_y, threshold=30)
        print("trace_result:", trace_result)
        if trace_result:
            delta_degree_x, delta_degree_y = trace_result
            print(f'delta_degree_x: {delta_degree_x}')
            print(f'delta_degree_y: {delta_degree_y}')
            buttom_servo.set_delta_degree(delta_degree_x)
            upper_servo.set_delta_degree(delta_degree_y)

        # degree = int(input("degree1 = "))
        # buttom_servo.set_pwm(degree)
        # degree = int(input("degree2 = "))
        # upper_servo.set_degree(degree)




    # =================== Infrared Sensor

    # from sensors import InfraredSensor
    # from utime import sleep
    # infra = InfraredSensor(14)
    # while True:
    #     sleep(0.1)
    #     print(infra.read())


    # =================== Microphone

    # from microphone import Microphone

    # mic = Microphone()
    # mic.record(seconds=5)