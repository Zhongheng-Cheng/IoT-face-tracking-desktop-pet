from socket import *

def receive_data_once():
    message = ''
    while '\n' not in message:
        message = connectionSocket.recv(1024).decode()
    return message

def send_data(message):
    connectionSocket.send(message.encode())
    return


serverPort = int(input("Server port: "))
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
connectionSocket, clientAddress = serverSocket.accept()
print("Connection established with ", clientAddress)
while True:
    try:
        message = receive_data_once()
        print(message)
    except KeyboardInterrupt:
        print("The server is ready to receive")
        connectionSocket, clientAddress = serverSocket.accept()
        print("Connection established with ", clientAddress)
