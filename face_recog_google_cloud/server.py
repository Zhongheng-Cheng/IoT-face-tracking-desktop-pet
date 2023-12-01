from socket import *

SOI = b'\xff\xd8' # Start of Image
SOS = b'\xff\xda' # Start of Scan
EOI = b'\xff\xd9' # End of Image

def receive_data_once():
    data = connectionSocket.recv(1024)
    if not data:
        raise 
    return data

def send_data(message):
    connectionSocket.send(message.encode())
    return

def receive_image():
    image_bytes = b''
    while not image_bytes.endswith(EOI):
        data = receive_data_once()
        if data.startswith(SOI):
            image_bytes = b''
        image_bytes += data
        if data.endswith(EOI):
            break
    return image_bytes


def rebuild_image(jpeg_bytes, path='downloaded_image.jpg'):
    from PIL import Image
    from io import BytesIO
    image_stream = BytesIO(jpeg_bytes)
    image = Image.open(image_stream).rotate(180)
    return image

def convert_pil_to_cv2(pil_image):
    import numpy
    pil_image = pil_image.convert('RGB')
    cv2_image = numpy.array(pil_image)
    cv2_image = cv2_image[:, :, ::-1].copy()
    return cv2_image

# def face_detect(image):
#     import cv2
#     # 加载特征文件
#     face_detector = cv2.CascadeClassifier('haarcascade_profileface.xml')
#     # 读取人脸图片
#     # face_im = cv2.imread('xscn.png')
#     face_im = image
#     # 灰度转换
#     grey = cv2.cvtColor(face_im, cv2.COLOR_BGR2GRAY)
#     # 检测人脸
#     faces = face_detector.detectMultiScale(grey)
#     # 遍历人脸
#     for x, y, w, h in faces:
#         # 在人脸区域绘制矩形
#         face_im = cv2.rectangle(face_im, (x, y), (x+w, y+h), (0, 255, 0), 5)
#     cv2.imwrite('cv2_image.jpg', face_im)
#     return faces

def face_detect(image):
    import cv2
    import numpy as np

    # 加载模型和配置文件
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt.txt', 'res10_300x300_ssd_iter_140000.caffemodel')

    # 获取图像尺寸
    (h, w) = image.shape[:2]
    startX, startY, endX, endY = 0, 0, 0, 0

    # 预处理图像：设置 blob 尺寸，进行归一化
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # 通过网络进行前向传播
    net.setInput(blob)
    detections = net.forward()
    
    # 循环检测到的人脸
    for i in range(0, detections.shape[2]):
        # 获取与检测相关的置信度（即概率）
        confidence = detections[0, 0, i, 2]

        # 过滤掉弱检测，确保置信度 > 最小置信度
        if confidence > 0.5:
            # 计算边界框的 (x, y) 坐标
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # 绘制边界框及置信度
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
            cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.imwrite('cv2_image.jpg', image)
    return startX, startY, endX, endY


serverPort = int(input("Server port: "))
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
connectionSocket, clientAddress = serverSocket.accept()
print("Connection established with ", clientAddress)
while True:
    try:
        image_bytes = receive_image()
        pil_image = rebuild_image(image_bytes)
        cv2_image = convert_pil_to_cv2(pil_image)
        face_location = face_detect(cv2_image)
        print(face_location)
        print("===============================")
    except Exception as e:
        print(e)
        print("The server is ready to receive")
        connectionSocket, clientAddress = serverSocket.accept()
        print("Connection established with ", clientAddress)
