from socket import *
from gest_predict import GestPredict

def receive_data_once():
    with open(csv_path, 'w') as fo:
        fo.seek(0)
        fo.truncate()
    message = ''
    while '\n' not in message:
        message = connectionSocket.recv(1024).decode()
        with open(csv_path, 'a') as fo:
            fo.write(message)

def send_data(message):
    connectionSocket.send(message.encode())

csv_path = "gest.csv"
gp = GestPredict()
serverPort = int(input("Server port: "))
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
connectionSocket, clientAddress = serverSocket.accept()
print("Connection established with ", clientAddress)
while True:
    try:
        receive_data_once()
        gp.read_data(csv_path)
        result = gp.predict()
        send_data(result)
    except KeyboardInterrupt:
        print("The server is ready to receive")
        connectionSocket, clientAddress = serverSocket.accept()
        print("Connection established with ", clientAddress)
