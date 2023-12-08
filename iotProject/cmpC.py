import cv2
import numpy as np

# 加载模型和配置文件
net = cv2.dnn.readNetFromCaffe('deploy.prototxt.txt', 'res10_300x300_ssd_iter_140000.caffemodel')

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

        # 前向传播
        net.setInput(blob)
        detections = net.forward()

        # 循环检测
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # 绘制边界框和置信度
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # 显示帧
        cv2.imshow("Frame", frame)

        # 按 'q' 退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
