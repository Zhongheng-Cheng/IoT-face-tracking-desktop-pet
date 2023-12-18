import subprocess
import time
import serial

class SerialReader(object):
    def __init__(self):
        self.wave_data = []

    def read(self):
        # 打开串口
        ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200)  # 请替换为实际的串口号和波特率

        try:
            while True:
                # 读取串口数据
                # data = ser.readline().decode('utf-8').strip()
                data = ser.readline()
                print(data)
                try:
                    # 处理接收到的数据
                    if data.startswith(b':::'):
                        commands_list = data.decode().split()
                        print(commands_list)
                        result = "Failed"
                        if "volume" in commands_list:
                            set_volume(int(commands_list[-1]))
                            result = "Success"
                        elif "mute" in commands_list:
                            mute()
                            result = "Success"
                        elif "unmute" in commands_list:
                            unmute()
                            result = "Success"
                        elif "open" in commands_list:
                            open_app(commands_list[-1])
                            result = "Success"
                        ser.write(result.encode())
                except Exception as e:
                    print(e)
                
        except KeyboardInterrupt:
            print("Serial communication terminated by user.")
        finally:
            # 关闭串口
            ser.close()
            return 

def set_volume(volume):
    try:
        # 使用 osascript 执行 AppleScript 设置音量
        subprocess.run(['osascript', '-e', f'set volume output volume {volume}'])
        print(f'Successfully set volume to {volume}%')
    except Exception as e:
        print(f'Error setting volume: {e}')

def mute():
    try:
        # 使用 osascript 执行 AppleScript 静音
        subprocess.run(['osascript', '-e', 'set volume with output muted'])
        print('Successfully muted')
    except Exception as e:
        print(f'Error muting: {e}')

def unmute():
    try:
        # 使用 osascript 执行 AppleScript 取消静音
        subprocess.run(['osascript', '-e', 'set volume without output muted'])
        print('Successfully unmuted')
    except Exception as e:
        print(f'Error unmuting: {e}')

def open_app(app_name):
    try:
        subprocess.run(['osascript', '-e', f'tell app "{app_name}" to activate'])
        print('Successfully unmuted')
    except Exception as e:
        print(f'Error unmuting: {e}')
    return

# # 设置音量为 50%
# set_volume(20)

# time.sleep(10)
# # 静音
# mute()
# time.sleep(10)
# # 取消静音
# unmute()

# open_app("spotify")
        
ser = SerialReader()
ser.read()
