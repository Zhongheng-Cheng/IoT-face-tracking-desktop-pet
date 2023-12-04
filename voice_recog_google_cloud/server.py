from socket import *
import wave
import array

def receive_data():
    received_data = []
    while True:
        message = connectionSocket.recv(2)
        if message != b'\n':
            data_high8 = int(message[0])
            data_low8 = int(message[1])
            data = (data_high8 << 8) + data_low8
            received_data.append(data)
        else:
            return received_data

def scale_and_offset(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def create_wav_file(wave_data, output_filename, sample_rate=8000, duration=1, frequency=440.0):
    num_frames = int(sample_rate * duration)

    # 创建 WAV 文件头
    with wave.open(output_filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位样本宽度
        wav_file.setframerate(sample_rate)
        wav_file.setnframes(num_frames)
        wav_file.setcomptype('NONE', 'not compressed')
        wav_file.writeframes(wave_data.tobytes())
    return

def plot(data1, data2):
    import matplotlib.pyplot as plt
    x_values = list(range(len(data1)))
    y1_values = data1
    y2_values = data2

    # 创建 Figure 对象和 Axes 对象（2行1列的布局）
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    # 在第一个 Axes 上绘制正弦图
    ax1.plot(x_values, y1_values)

    # 在第二个 Axes 上绘制余弦图
    ax2.plot(x_values, y2_values)

    # 调整布局，以防止重叠
    plt.tight_layout()

    # 显示图像
    plt.show()

def send_data(message):
    connectionSocket.send(message.encode())

csv_path = "voice_wav.csv"
serverPort = int(input("Server port: "))
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print("The server is ready to receive")
    connectionSocket, clientAddress = serverSocket.accept()
    print("Connection established with ", clientAddress)
    raw_data = receive_data()
    wave_data = array.array('h', [scale_and_offset(i, 0, 1023, -32768, 32767) for i in raw_data])
    # plot(raw_data, wave_data)
    create_wav_file(wave_data, 'output.wav')
