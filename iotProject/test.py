import socket
import cv2
import io
from PIL import Image
import numpy as np

# 创建套接字
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind(("0.0.0.0", 9091))  # 绑定你电脑上的所有IP地址，如果电脑有多个IP地址，数据都接收

while True:
    data, IP = s.recvfrom(100000)  # 接收数据，设置数据包大小。图片大小100K
    bytes_stream = io.BytesIO(data)  # 收到数据后转为字节流
    image = Image.open(bytes_stream)  # 打开这个图片
    img = np.asarray(image)  # 转化为数组格式
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）
    cv2.imshow("ESP32 Capture Image", img)  # 显示图片
    if cv2.waitKey(1) == ord("q"):  # 按键盘上的q键，退出
        break