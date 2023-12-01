# import time
# from sensors import LightSensor, Accelerometer
# from button import Button
# from rtc_clock import RTC_Clock
# from networks import NetworkConn, API
# from display import OLED
# from server import Server
# from gesture_recog import GestureRecg

# class State_Machine(object):
#     def __init__(self):
#         self.states = ["SHOW_TIME", "SET_TIME", "SET_ALARM", "CONFIRM_ALARM", "GESTURE", "VOICE", "ALARM_RINGING!!!"]
#         self.main_state_loop = ["SHOW_TIME", "SET_TIME", "SET_ALARM", "CONFIRM_ALARM", "GESTURE"]
#         self.current = 0
#         return

#     def current_state(self):
#         '''
#         Output:
#             str: current state name
#         '''
#         return self.states[self.current]
    
#     def next_state(self):
#         '''
#         Loop among ["SHOW_TIME", "SET_TIME", "SET_ALARM", "CONFIRM_ALARM", "GESTURE"]
#         '''
#         self.current = (self.current + 1) % (len(self.main_state_loop))
#         print("Switched state to", self.current_state())
#         if sm.current_state() == "SET_TIME":
#             clock.current_time_setter = clock.hhmmss_fields[0]
#             return

#         elif sm.current_state() == "SET_ALARM":
#             clock.current_alarm_setter = clock.hhmmss_fields[0]
#             return
        
#         elif sm.current_state() == "GESTURE":
#             global gestureMessage
#             gestureRecog.serverConnection()
#             gestureMessage = ''
#             return

#     def jump_to_state(self, state="SHOW_TIME"):
#         '''
#         Input:
#             state: str; ["SHOW_TIME", "SET_TIME", "SET_ALARM", "CONFIRM_ALARM", "GESTURE", "VOICE", "ALARM_RINGING!!!"]
#         '''
#         assert state in self.states
#         self.current = self.states.index(state)
#         print("Switched state to", self.current_state())
#         return
    

# def switch_states(p):
#     '''
#     Switching states
#     ALARM_RINGING!!!: Turn off alarm and jump to SHOW_TIME
#     '''
#     global gestureMessage
#     if sm.current_state() == "ALARM_RINGING!!!":
#         sm.jump_to_state("SHOW_TIME")
#         clock.alarm.value(1)
#         return

#     elif sm.current_state() == "VOICE":
#         sm.jump_to_state("SHOW_TIME")
#         return

#     # All states except ALARM_RINGING!!!
#     else:
#         sm.next_state()

# def button1_short(p):
#     '''
#     SET_TIME: +1
#     SET_ALARM: +1
#     CONFIRM_ALARM: Confirm
#     ALARM_RINGING!!!: Turn off alarm and jump to SHOW_TIME
#     GESTURE: Start recognition
#     '''
#     if sm.current_state() == "SET_TIME":
#         clock.inc_time_element(clock.current_time_setter)
#         print("Button B pressed and set time %s +1" % (clock.current_time_setter))
#         return

#     if sm.current_state() == "SET_ALARM":
#         clock.inc_alarm_element(clock.current_alarm_setter)
#         print("Button B pressed and set alarm %s +1" % (clock.current_alarm_setter))
#         return

#     if sm.current_state() == "CONFIRM_ALARM":
#         clock.alarm_enable(callback_alarm)
#         print("Alarm enabled")
#         sm.next_state()
#         return

#     if sm.current_state() == "ALARM_RINGING!!!":
#         sm.jump_to_state("SHOW_TIME")
#         clock.alarm.value(1)
#         return

#     global gestureMessage
#     if sm.current_state() == "GESTURE":
#         gestureMessage = gestureRecog.button_pressed()
#         return

# def voice_state(p):
#     global voice_message, voice_result
#     sm.jump_to_state("VOICE")
#     voice_message = ''
#     voice_result = ''
#     return

# def button2_short(p):
#     '''
#     SET_TIME: Shift
#     SET_ALARM: Shift
#     CONFIRM_ALARM: Cancel alarm
#     ALARM_RINGING!!!: Turn off alarm and jump to SHOW_TIME
#     '''

#     if sm.current_state() == "SET_TIME":
#         time_index = clock.hhmmss_fields.index(clock.current_time_setter)
#         time_index = (time_index + 1) % 3
#         clock.current_time_setter = clock.hhmmss_fields[time_index]
#         print("Button C pressed and the current setting is", clock.current_time_setter)
#         return

#     if sm.current_state() == "SET_ALARM":
#         alarm_index = clock.hhmmss_fields.index(clock.current_alarm_setter)
#         alarm_index = (alarm_index + 1) % 3
#         clock.current_alarm_setter = clock.hhmmss_fields[alarm_index]
#         print("Button C pressed and the current setting is", clock.current_alarm_setter)
#         return

#     if sm.current_state() == "CONFIRM_ALARM":
#         clock.cancel_alarm()
#         print("Alarm cancelled")
#         sm.next_state()
#         return

#     if sm.current_state() == "ALARM_RINGING!!!":
#         sm.jump_to_state("SHOW_TIME")
#         clock.alarm.value(1)
#         return


# def callback_alarm():
#     '''
#     Callback function for alarm
#     '''
#     clock.alarm.value(0)
#     sm.jump_to_state("ALARM_RINGING!!!")
#     return


# def make_display_content():
#     global gestureMessage
#     time_text = ":".join([str(i) for i in clock.get_now_time()])

#     if (sm.current_state() in ["SET_ALARM", "CONFIRM_ALARM"]) or clock.is_alarm_on:
#         alarm_text = ":".join([str(i) for i in clock.get_alarm_time()])
#     else:
#         alarm_text = ''

#     if sm.current_state() == "SET_TIME":
#         line1 = "SET_TIME: " + clock.current_time_setter
#         line2 = time_text + alarm_text
#         line3 = '1:+1,2:shift'
#     elif sm.current_state() == "SET_ALARM":
#         line1 = "SET_ALARM: " + clock.current_alarm_setter
#         line2 = time_text + alarm_text
#         line3 = '1:+1,2:shift'
#     elif sm.current_state() == "CONFIRM_ALARM":
#         line1 = "CONFIRM ALARM"
#         line2 = time_text + alarm_text
#         line3 = '1:YES,2:CANCEL'
#     elif sm.current_state() == "GESTURE":
#         line1 = "GESTURE: " + gestureMessage
#         line2 = ''
#         line3 = ''
#     elif sm.current_state() == "VOICE":
#         line1 = "VOICE RECOG"
#         line2 = voice_message
#         line3 = voice_result
#     else:
#         line1 = sm.current_state()
#         line2 = time_text + alarm_text
#         line3 = ''

#     content = [
#         [line1, 0, 0, 1],
#         [line2, 0, 10, 1],
#         [line3, 0, 20, 1],
#     ]

#     return content

# def check_message(message) -> str:
#     message_words = message.split()
#     if "on" in message_words and "screen" in message_words:
#         screen.is_on = True
#         return "Successful"
#     elif "off" in message_words and "screen" in message_words:
#         screen.is_on = False
#         return
#     elif "time" in message_words:
#         sm.jump_to_state("SHOW_TIME")
#         return "Successful"
#     elif "weather" in message_words:
#         api_get = api.get_weather()
#         return api_get['weather'][0]['main'] + str(api_get['main']['temp'])
#     elif 'location' in message_words:
#         api_get = api.get_geolocation()
#         return api_get["city"]
#     elif message == '':
#         return ''
#     else:
#         return "Failed"

# def smart_watch_work():
#     global screen
#     global voice_message, voice_result
#     while True:
#         clock.check_alarm()
#         light_sensor.check_light_value()
#         screen.display.contrast(light_sensor.light_value)
#         content = make_display_content()
#         screen.show_text(content)
#         time.sleep_ms(1)
#         if sm.current_state() == "VOICE":
#             voice_message = server.receive_once()
#             print("Voice message received: " + voice_message)
#             voice_result = check_message(voice_message)


# if __name__ == '__main__':
#     # init
#     sm = State_Machine()
#     nc = NetworkConn()
#     light_sensor = LightSensor(adc=0)
#     screen = OLED(pin_sda=4, pin_scl=5)
#     accel = Accelerometer()
#     api = API()
#     hh, mm, ss = api.get_realtime()
#     clock = RTC_Clock(hour=hh, minute=mm, second=ss)
#     clock.set_alarm(pin_alarm=16, hour=0, minute=0, second=0)
#     buttonA = Button(pin=0, long_press=switch_states, release=button1_short)
#     buttonC = Button(pin=2, long_press=voice_state, release=button2_short)
#     gestureRecog = GestureRecg(accel)
#     server = Server()
#     server.config_listening(8012)

#     smart_watch_work()


from servo import Servo
buttom_servo = Servo(pin=14, static_err=-8)
upper_servo = Servo(pin=12)
while True:
    degree = int(input("degree = "))
    buttom_servo.set_pwm(degree)
    upper_servo.set_pwm(90)

# from networks import NetworkConn
# network_conn = NetworkConn()

# from display import ST7789_Controller
# display = ST7789_Controller(CS_PIN=13, 
#                             DC_PIN=15,
#                             )
# display.test()

# from sensors import InfraredSensor
# from utime import sleep
# infra = InfraredSensor(14)
# while True:
#     sleep(0.1)
#     print(infra.read())