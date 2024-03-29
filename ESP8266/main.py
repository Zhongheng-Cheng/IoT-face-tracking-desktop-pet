from networks import NetworkConn, API
from servo import Servo
from display import OLED
from rtc_clock import RTC_Clock
from finite_state_machine import FiniteStateMachine
from button import Button
from server import Server
from sensors import InfraredSensor
import usocket
import utime
from urequests import post

SERVER_IP = "35.188.219.151"
FACE_SERVER_PORT = 8012
DATABASE_SERVER_PORT = 8000

def button_short(p):
    '''
    Any state except VOICE_RECOG: jump to VOICE_RECOG
    VOICE_RECOG: jump to MAIN
    '''
    if fsm.current_state != "VOICE_RECOG":
        fsm.jump_to_state("VOICE_RECOG")
        return
    
    if fsm.current_state == "VOICE_RECOG":
        fsm.jump_to_state("MAIN")
        return

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

def make_display_content(state):
    line1 = line2 = line3 = ''

    if state == "MAIN":
        line1 = ":".join([str(i) for i in clock.get_now_time()])
        line2 = weather_text
        line3 = ''
    
    if state == "SHOW_QUOTE":
        line1 = quote_get['quote']
        line2 = ''
        line3 = quote_get['author']
    
    if state == "VOICE_RECOG":
        line1 = "VOICE_RECOG"
        line2 = voice_message
        line3 = ''

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
    api = API()

    print("Retrieving real time...")
    year, month, day, hh, mm, ss = api.get_full_realtime()
    clock = RTC_Clock(year=year, month=month, day=day, hour=hh, minute=mm, second=ss)

    print("Retrieving weather info...")
    weather_get = api.get_weather()
    weather_text = weather_get['weather'][0]['main'] + str(weather_get['main']['temp'])

    print("Connecting to server...")
    nc.connect_to_server(SERVER_IP, FACE_SERVER_PORT)
    nc.clientSocket.settimeout(5)

    print("Initializing accessories...")
    buttom_servo = Servo(pin=12, static_err=-8)
    upper_servo = Servo(pin=14, degree_limit=[90, 180])
    screen = OLED(pin_sda=4, pin_scl=5)
    
    fsm = FiniteStateMachine()
    button = Button(pin=0, release=button_short)
    ir = InfraredSensor(pin=13)
    
    print("Initializing server on chip...")
    server = Server()
    server.config_listening(8012)
    
    start_time = None
    stop_time = None

    is_sitting = False

    voice_message = ''

    # clear unused buffer
    center = nc.clientSocket.recv(2048)

    # main working logic
    while True:
        content = make_display_content(fsm.current_state)
        screen.show_text(content)
        if ir.is_detect():
            if fsm.current_state == "MAIN" or fsm.current_state == "SHOW_QUOTE":
                time_text = ":".join([str(i) for i in clock.get_now_time()])
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
                                utime.sleep_ms(1)
                        else:
                            if is_sitting:
                                is_sitting = False
                                end_time = clock.get_now_iso_time()

                                # send data to database
                                post_sitting_data(start_time, end_time)
                                utime.sleep_ms(1)
                                
                # except usocket.timeout:
                #     pass
                except Exception as e:
                    print(e)
                    # nc = NetworkConn()
                    # nc.connect_to_server(SERVER_IP, FACE_SERVER_PORT)
        else:
            center = nc.clientSocket.recv(2)
            print("Not excuted: ", center)
        
        if fsm.current_state == "VOICE_RECOG":
            if voice_message != '':
                utime.sleep(3)
                fsm.jump_to_state("MAIN")
                voice_message = ''
                continue
            print("VOICE_RECOG mode")
            voice_message = server.receive_once()
            if voice_message != "":
                print("::: " + voice_message)
                # result = input()
            # voice_result = check_message(voice_message) ###try# voice_result = input()
        