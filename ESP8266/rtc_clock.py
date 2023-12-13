from machine import Pin, RTC

class RTC_Clock(object):
    def __init__(self, hour: int, minute: int, second: int):
        '''
        Initial time setting: hour, minute, second
        Hard-coded fields:
            year = 2023
            month = 1
            day = 1
            weekday = 7
            microsecond = 0
        '''
        self.rtc = RTC()
        self.rtc.datetime([2023, 1, 1, 7, hour, minute, second, 0])
        self.time_fields = ['year', 'month', 'day', 'weekday', 'hour', 'minute', 'second']
        self.hhmmss_max = [24, 60, 60]
        self.hhmmss_fields = ["hour", "minute", "second"]
        self.current_time_setter = self.hhmmss_fields[0]
        self.current_alarm_setter = self.hhmmss_fields[0]
        self.alarm_time = [0, 0, 0]
        self.is_alarm_on = False
        return

    def get_now_time(self) -> list:
        '''
        Output: 
            list: [hour, minute, second]
        '''
        return list(self.rtc.datetime()[4:7])
    
    def get_now_iso_time(self) -> str:
        rtc_time = self.rtc.datetime()
        iso_time = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(
            rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[4], rtc_time[5], rtc_time[6]
        )
        return iso_time

    def inc_time_element(self, field: str = 'hour'):
        '''
        Increment a time tuple element by 1.
        Fields: ['year', 'month', 'day', 'weekday', 'hour', 'minute', 'second']
        '''
        assert field in self.time_fields
        datetime = list(self.rtc.datetime())
        field_index = self.time_fields.index(field)
        if field_index in [4, 5, 6]:
            datetime[field_index] = (datetime[field_index] + 1) % self.hhmmss_max[field_index - 4]
        else:
            datetime[field_index] += 1
        self.rtc.datetime(tuple(datetime))
        return
    
    def inc_alarm_element(self, field: str = "hour"):
        '''
        Increment an alarm tuple element by 1.
        Fields: ["hour", "minute", "second"]
        '''
        assert field in self.hhmmss_fields
        field_index = self.hhmmss_fields.index(field)
        self.alarm_time[field_index] = (self.alarm_time[field_index] + 1) % self.hhmmss_max[field_index]
        return
    
    def set_alarm(self, 
                  pin_alarm: int = None, 
                  hour: int = None, 
                  minute: int = None, 
                  second: int = None):

        self.alarm = Pin(pin_alarm, Pin.OUT)
        self.alarm.value(1)
        self.alarm_time = [hour, minute, second]
        return

    def set_timer(self, time_in_s: int) -> str:
        '''
        Input:
            time_in_s: int; in seconds
        Output:
            str: Alarm status info
        '''
        self.alarm_time = time_in_s * 1000
        return
    
    def get_alarm_time(self) -> list:
        '''
        Output:
            list: [hour, minute, second]
        '''
        if type(self.alarm_time) == "int":
            return [self.alarm_time]
        else:
            return self.alarm_time

    def alarm_left(self) -> int:
        '''
        Output:
            int: Number of seconds left before the alarm expires
        '''
        return self.rtc.alarm_left() // 1000
    
    def alarm_enable(self, handler=None):
        '''
        Input:
            handler: callback function
        '''
        self.is_alarm_on = True
        self.alarm_handler = handler
        return
    
    def cancel_alarm(self):
        self.is_alarm_on = False
        return

    def check_alarm(self):
        '''
        If now_time reaches alarm_time, enter alarm_handler
        '''
        if self.get_now_time() == self.get_alarm_time():
            self.is_alarm_on = False
            self.alarm_handler()
        return