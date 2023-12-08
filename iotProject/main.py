import serial
import cv2
import numpy as np
import io
from PIL import Image
import codecs
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # 设置超时，防止长时间阻塞

while True:
    data = ser.readline()
    data = bytes(data[2:-3], encoding="utf-8")
    original = codecs.escape_decode(data, "hex-escape")
    print(original)
    # bytes_stream = io.BytesIO(data)  # 收到数据后转为字节流
    # image = Image.open(bytes_stream)  # 打开这个图片
    # img = np.asarray(image)  # 转化为数组格式
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）
    # cv2.imshow("ESP32 Capture Image", img)  # 显示图片
    # if cv2.waitKey(1) == ord("q"):  # 按键盘上的q键，退出
    #     break
    # 将字节数据转换为 numpy 数组
    # nparr = np.frombuffer(data, np.uint8)

    # 使用 cv2.imdecode 解码图像
    # 第二个参数是一个标志，cv2.IMREAD_COLOR 表示将图像转换为彩色图像
    # image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #
    # # 检查图像是否正确加载
    # if image is not None:
    #     # 显示图像
    #     cv2.imshow('Image', image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    # else:
    #     print("无法解码图像")