from socket import *
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from io import BytesIO

# Constants for image processing
SOI = b'\xff\xd8'  # Start of Image
EOI = b'\xff\xd9'  # End of Image
CAMERA_PORT = 8015
SERVO_PORT = 8012
SCREEN_PORT = 8013
# Load face detection model
face_net = cv2.dnn.readNetFromCaffe('deploy.prototxt.txt', 'res10_300x300_ssd_iter_140000.caffemodel')

# Load emotion recognition model
emotion_model = load_model('simple_CNN.985-0.66.hdf5')
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Surprise", "Sad"]

def receive_data_once():
    data, address = serverSocket.recvfrom(100000)
    print(len(data))
    if not data:
        raise
    return data
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


def detect_face(image):
    # Perform face detection and return face location
    (h, w) = image.shape[:2]
    startX, startY, endX, endY = 0, 0, 0, 0

    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

    return startX, startY, endX, endY

def send_data_to_client(data, connection_socket):
    # Send data to the client over the socket connection
    connection_socket.send(data.encode())


def rebuild_image(jpeg_bytes):
    image_stream = BytesIO(jpeg_bytes)
    image = Image.open(image_stream)
    image.save("PIL_image.jpg")
    return image


def convert_pil_to_cv2(pil_image):
    pil_image = pil_image.convert('RGB')
    cv2_image = np.array(pil_image)
    cv2_image = cv2_image[:, :, ::-1].copy()
    return cv2_image

def find_center(face_location):
    startX, startY, endX, endY = face_location
    center_x = (startX + endX) // 2
    center_y = (startY + endY) // 2
    return center_x, center_y


def emotion(img, face_location):
    #img = cv2.imread("PIL_image.jpg")
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    # Ensure face_location is a list even if there's only one face
    if not isinstance(face_location, list):
        face_location = [face_location]

    for (x, y, w, h) in face_location:
        gray_face = gray[y:y + h, x:x + w]  # Fix the indexing here

        gray_face = cv2.resize(gray_face, (48, 48))
        gray_face = gray_face / 255.0
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_label_arg = np.argmax(emotion_model.predict(gray_face))
        emotion = emotion_labels[emotion_label_arg]
        #print(emotion)
    return emotion


# Your main server code here
# UDP for camera
serverSocket = socket(AF_INET, SOCK_DGRAM, 0)
serverSocket.bind(('', CAMERA_PORT))
print("The server is ready to receive from camera")

# TCP for SCREEN
screenSocket = socket(AF_INET, SOCK_STREAM)
screenSocket.bind(('', SCREEN_PORT))
screenSocket.listen(1)
print("The server is ready to receive from screen")
connectionSocket1, clientAddress1 = screenSocket.accept()
print("Connection established with ", clientAddress1)

# TCP for SERVO
servoSocket = socket(AF_INET, SOCK_STREAM)
servoSocket.bind(('', SERVO_PORT))
servoSocket.listen(1)
print("The server is ready to receive from camera")
connectionSocket2, clientAddress2 = servoSocket.accept()
print("Connection established with ", clientAddress2)


while True:
    try:
        image_bytes = receive_image()
        pil_image = rebuild_image(image_bytes)
        cv2_image = convert_pil_to_cv2(pil_image)
        #Face detection
        face_location = detect_face(cv2_image)
        # Emotion recognition
        face_emotion = emotion(pil_image, face_location)
        connectionSocket1.send(face_emotion.encode())
        #  Send data to the client
        center_point = find_center(face_location)
        connectionSocket2.send(bytearray(center_point))
    except Exception as e:
        print(e)
        # connectionSocket2.close()
        # print("The server is ready to receive")
        # connectionSocket2, clientAddress = serverSocket2.accept()
        # print("Connection established with ", clientAddress)
