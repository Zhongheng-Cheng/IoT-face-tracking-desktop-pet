from socket import *

def receive_data_once():
    with open(csv_path, 'w') as fo:
        fo.seek(0)
        fo.truncate()
    message = ''
    # while b'\n' not in message:
    while True:
        message = connectionSocket.recv(1024)
        for i in message[:5]:
            print(i)
        print("=====================")
        # with open(csv_path, 'a') as fo:
        #     fo.write(message)

def send_data(message):
    connectionSocket.send(message.encode())

csv_path = "voice_wav.csv"
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
    except KeyboardInterrupt:
        print("The server is ready to receive")
        connectionSocket, clientAddress = serverSocket.accept()
        print("Connection established with ", clientAddress)
