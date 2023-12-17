import network
from urequests import get, post
from ujson import loads
from os import listdir
from socket import *

# from requests import get
# from json import loads

class NetworkConn(object):
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.saved_wifi = self._get_saved_wifi()
        self.nearby_wifi = [i[0].decode() for i in self.wlan.scan()]
        for i in self.saved_wifi:
            if i[0] in self.nearby_wifi:
                self.do_connect(i[0], i[1])
                if self.wlan.isconnected():
                    break
        assert self.wlan.isconnected()
        return

    def _get_saved_wifi(self):
        if "_wifi_info.py" in listdir():
            import _wifi_info
            wifi_list = _wifi_info.ssid_key_pairs
        else:
            ssid = input('ssid: ')
            key = input('key: ')
            wifi_list = [[ssid, key]]
        return wifi_list

    def do_connect(self, ssid: str, key: str):
        time_count = 0
        if not self.wlan.isconnected():
            print('connecting to network %s...' % ssid)
            self.wlan.connect(ssid, key)
            while not self.wlan.isconnected():
                time_count += 1
                if time_count == 200000:
                    return
        print('network config:', self.wlan.ifconfig())
        self.ip = self.wlan.ifconfig()[0] # IP address, subnet mask, gateway and DNS server
        return
    
    def connect_to_server(self, server_name, server_port):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((server_name, server_port))
        print("Successfully connected")
        return

class API(object):
    def __init__(self):
        self.weather_API_key = "f485ffaf9f59c68087e74f169c50068f"
        self.quote_API_key = "eGE3BW/+7sbstu2WTj932A==LpbbfCm49dQxm9rf"
        self.latitude = self.longitude = None
        return

    def send_ntfy(self, topic_name: str, message: str):
        url = "http://ntfy.sh/%s" % topic_name
        post(url=url, data=message)
        return

    def get_geolocation(self) -> dict:
        '''
        example response:
        {
            'status': 'success', 
            'country': 'United States', 
            'countryCode': 'US', 
            'region': 'NY', 
            'regionName': 'New York', 
            'city': 'Queens', 
            'zip': '11101', 
            'lat': 40.7429, 
            'lon': -73.9392, 
            'timezone': 'America/New_York', 
            'isp': 'Verizon Business', 
            'org': 'Verizon Business', 
            'as': 'AS701 Verizon Business', 
            'query': '68.237.211.156'
        }
        '''
        url = "http://ip-api.com/json"
        geo_data_get = get(url)
        geo_data = loads(geo_data_get.text)
        self.latitude = geo_data["lat"]
        self.longitude = geo_data["lon"]
        return geo_data


    def get_weather(self) -> dict:
        '''
        example response:
        {
            'coord': {'lon': -73, 'lat': 40}, 
            'weather': [{
                'id': 800, 
                'main': 'Clear', 
                'description': 'clear sky', 
                'icon': '01n'
            }], 
            'base': 'stations', 
            'main': {
                'temp': 15.88, 
                'feels_like': 15.51, 
                'temp_min': 15.88, 
                'temp_max': 15.88, 
                'pressure': 1028, 
                'humidity': 76, 
                'sea_level': 1028, 
                'grnd_level': 1028
            }, 
            'visibility': 10000, 
            'wind': {
                'speed': 6.68, 
                'deg': 210, 
                'gust': 7.61
            }, 
            'clouds': {
                'all': 3
            }, 
            'dt': 1698200201, 
            'sys': {
                'country': 
                'US', 
                'sunrise': 1698145899, 
                'sunset': 1698184830
            }, 
            'timezone': -18000, 
            'id': 5119232, 
            'name': 'Great River', 
            'cod': 200
        }
        '''
        if not self.latitude or not self.longitude:
            self.get_geolocation()

        url = "http://api.openweathermap.org/data/2.5/weather?lat=%2d&lon=%2d&appid=%s&units=%s" \
            % (self.latitude, 
               self.longitude, 
               self.weather_API_key, 
               "metric") # units:standard (default), metric (Celsius), imperial (Fehrenheit))
        weather_data_get = get(url)
        weather_data = loads(weather_data_get.text)
        return weather_data
    
    def get_realtime_api(self) -> dict:
        '''
        example response:
        {
            'abbreviation': 'EDT', 
            'client_ip': '2600:4041:582c:f200:d927:c9b7:f008:6f3e', 
            'datetime': '2023-10-24T22:22:25.906542-04:00', 
            'day_of_week': 2, 
            'day_of_year': 297, 
            'dst': True, 
            'dst_from': '2023-03-12T07:00:00+00:00', 
            'dst_offset': 3600, 
            'dst_until': '2023-11-05T06:00:00+00:00', 
            'raw_offset': -18000, 
            'timezone': 'America/New_York', 
            'unixtime': 1698200545, 
            'utc_datetime': '2023-10-25T02:22:25.906542+00:00', 
            'utc_offset': '-04:00', 
            'week_number': 43
        }
        '''
        url = "http://worldtimeapi.org/api/timezone/America/New_York"
        time_data_get = get(url)
        time_data = loads(time_data_get.text)
        return time_data
    
    def get_realtime(self) -> list:
        '''
        Output format
            [hh: int, mm: int, ss: int]
        '''
        hour, minute, second = [int(i) for i in self.get_realtime_api()["datetime"][11:19].split(':')]
        return [hour, minute, second]
    
    def get_full_realtime(self) -> list:
        time_text = self.get_realtime_api()["datetime"]
        year = int(time_text[0:4])
        month = int(time_text[5:7])
        day = int(time_text[8:10])
        hour, minute, second = [int(i) for i in time_text[11:19].split(':')]
        return [year, month, day, hour, minute, second]

    def get_quote(self, category: str) -> dict:
        '''
        See full possible categories at:
        https://api-ninjas.com/api/quotes

        Output:
        {
            'quote': str,
            'author': str
        }
        '''
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
        response = get(api_url, headers={'X-Api-Key': self.quote_API_key})
        if response.status_code == 200:
            res = loads(response.text)[0]
            return res
        else:
            print("Error:", response.status_code, response.text)
            return 