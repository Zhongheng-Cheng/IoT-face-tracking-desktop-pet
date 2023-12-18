import subprocess
import time

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

# # 设置音量为 50%
# set_volume(20)

# time.sleep(10)
# # 静音
# mute()
# time.sleep(10)
# # 取消静音
# unmute()

open_app("spotify")