import cv2
import numpy as np
from tensorflow.keras.models import load_model

# 加载人脸检测模型和配置文件
face_net = cv2.dnn.readNetFromCaffe('deploy.prototxt.txt', 'res10_300x300_ssd_iter_140000.caffemodel')

# 加载表情识别模型
emotion_model = load_model('simple_CNN.985-0.66.hdf5')

# 定义表情类别
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# 打开视频源，0 通常代表摄像头
cap = cv2.VideoCapture(0)

if __name__ == '__main__':
    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            break

        # 获取帧的尺寸
        (h, w) = frame.shape[:2]

        # 预处理帧
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        # 前向传播进行人脸检测
        face_net.setInput(blob)
        detections = face_net.forward()
        # 循环检测
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # 提取人脸区域
                face = frame[startY:endY, startX:endX]

                # 预处理人脸图像，例如调整大小和归一化
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                face = face/255.0
                face = np.expand_dims(face, axis=0)

                # 使用表情识别模型进行预测
                emotion_pred = emotion_model.predict(face)
                emotion_label = emotion_labels[np.argmax(emotion_pred)]

                # 绘制人脸边界框
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

                # 绘制表情标签
                cv2.putText(frame, emotion_label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # 显示帧
        cv2.imshow("Frame", frame)

        # 按 'q' 退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
