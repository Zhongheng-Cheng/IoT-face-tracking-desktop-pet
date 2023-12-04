import serial

class SerialReader(object):
    def __init__(self):
        pass

    def read(self):
        # 打开串口
        ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200)  # 请替换为实际的串口号和波特率

        try:
            transmission_flag = False
            wave_data = []
            while True:
                # 读取串口数据
                # data = ser.readline().decode('utf-8').strip()
                data = ser.readline()

                # 处理接收到的数据
                if data == b'start\r\n':
                    transmission_flag = True
                elif transmission_flag:
                    wave_data.append(data.strip())
                elif data.startswith(b'==='):
                    transmission_flag == False
                    print(data)
                    break
                
        except KeyboardInterrupt:
            print("Serial communication terminated by user.")
        finally:
            # 关闭串口
            ser.close()
            return