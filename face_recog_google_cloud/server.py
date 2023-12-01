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
    image = Image.open(image_stream)
    image.save(path)
    return

serverPort = int(input("Server port: "))
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
serverSocket.settimeout(5)
print("The server is ready to receive")
connectionSocket, clientAddress = serverSocket.accept()
print("Connection established with ", clientAddress)
while True:
    try:
        image_bytes = receive_image()
        rebuild_image(image_bytes)
        print("===============================")
    except Exception as e:
        print(e)
        print("The server is ready to receive")
        connectionSocket, clientAddress = serverSocket.accept()
        print("Connection established with ", clientAddress)
