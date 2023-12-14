from networks import NetworkConn, API
from servo import Servo
from display import OLED
from rtc_clock import RTC_Clock
import usocket
import utime
from urequests import post

SERVER_IP = "34.123.196.184"
FACE_SERVER_PORT = int(input("Face server port: "))
DATABASE_SERVER_PORT = int(input("Database server port: "))

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

def make_display_content(line2=None, line3=None):
    time_text = ":".join([str(i) for i in clock.get_now_time()])

    line1 = time_text
    if not line2:
        line2 = 'testline2'
    if not line3:
        line3 = 'testline3'

    content = [
        [line1, 0, 0, 1],
        [line2, 0, 10, 1],
        [line3, 0, 20, 1],
    ]

    return content

def post_sitting_data(start_time, end_time):
    url = f"http://{SERVER_IP}:{DATABASE_SERVER_PORT}/sitting-time?start_time={start_time}&end_time={end_time}"
    response = post(url)
    if response.status_code != 200:
        print(f"Error: {response.content}")
        print("Request URL:", response.request.url)
        print("Request Headers:", response.request.headers)
        print("Request Body:", response.request.body)
        return response
    return

if __name__ == '__main__':
    # init settings
    nc = NetworkConn()
    nc.connect_to_server(SERVER_IP, FACE_SERVER_PORT)
    # nc.clientSocket.settimeout(0.1)

    buttom_servo = Servo(pin=12, static_err=-8)
    upper_servo = Servo(pin=14, degree_limit=[90, 180])

    screen = OLED(pin_sda=4, pin_scl=5)
    api = API()
    year, month, day, hh, mm, ss = api.get_full_realtime()
    print(year, month, day, hh, mm, ss)
    clock = RTC_Clock(year=year, month=month, day=day, hour=hh, minute=mm, second=ss)
    start_time = None
    stop_time = None

    is_sitting = False

    # main working logic
    while True:
        
        # read and process face tracking data
        try:
            # get face position data
            center = nc.clientSocket.recv(2)
            center_x = int(center[0])
            center_y = int(center[1])
            print(f"location: ({center_x}, {center_y})")

            # adjust servos
            trace_result = trace_center(center_x, center_y, threshold=30)
            if trace_result:
                delta_degree_x, delta_degree_y = trace_result
                print(f'delta_degree: ({delta_degree_x}, {delta_degree_y})')
                buttom_servo.set_delta_degree(delta_degree_x)
                upper_servo.set_delta_degree(delta_degree_y)
                print(f"Buttom_servo degree: {buttom_servo.degree}")
                print(f'Upper_servo degree: {upper_servo.degree}')
                print()

                # check sitting state
                if upper_servo.degree < 130:
                    if not is_sitting:
                        is_sitting = True
                        start_time = clock.get_now_iso_time()
                        content = make_display_content(line2=start_time)
                        print(content)
                        screen.show_text(content)
                        utime.sleep_ms(1)
                else:
                    if is_sitting:
                        is_sitting = False
                        end_time = clock.get_now_iso_time()

                        # send data to database
                        post_sitting_data(start_time, end_time)
                        content = make_display_content(line2=start_time, line3=end_time)
                        screen.show_text(content)
                        utime.sleep_ms(1)
                        
        # except usocket.timeout:
        #     pass
        except Exception as e:
            print(e)
        




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