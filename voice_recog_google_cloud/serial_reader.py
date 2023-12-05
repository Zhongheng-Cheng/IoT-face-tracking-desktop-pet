import serial

class SerialReader(object):
    def __init__(self):
        self.wave_data = []

    def read(self):
        # 打开串口
        ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200)  # 请替换为实际的串口号和波特率

        try:
            transmission_flag = False
            while True:
                # 读取串口数据
                # data = ser.readline().decode('utf-8').strip()
                data = ser.readline()
                # print(data)

                # 处理接收到的数据
                if data.startswith(b'sample'):
                    transmission_flag == False
                    sample_rate = ser.readline().strip()
                    break
                elif transmission_flag:
                    self.wave_data.append(data)
                    # print(data)
                elif b'start' in data:
                    transmission_flag = True
                    print("Transmission started")
                
        except KeyboardInterrupt:
            print("Serial communication terminated by user.")
        finally:
            # 关闭串口
            ser.close()
            return self.wave_data, sample_rate