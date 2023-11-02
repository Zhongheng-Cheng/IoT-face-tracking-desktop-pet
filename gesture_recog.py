from socket import *
import utime

class GestureRecg:
    def __init__(self, accel):
        self.accel = accel

    def button_pressed(self):
        self.detect()
        message = self.clientSocket.recv(1024).decode()
        return message

    def detect(self):
        print("Detecting starts")
        for i in range(150):
            accel_data = self.accel.read_data()
            message = "%d, %d, %d" % (accel_data[0], accel_data[1], accel_data[2])
            if i == 149:
                message += '\n'
            else:
                message += ', '
            self.clientSocket.send(message.encode())
            utime.sleep_ms(20)
        print("Detecting ends")
        return

    def serverConnection(self):
        # server connection in callback_c long press
        serverName = "35.193.232.219"
        serverPort = 8011
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))
        print("Successfully connected")

        return