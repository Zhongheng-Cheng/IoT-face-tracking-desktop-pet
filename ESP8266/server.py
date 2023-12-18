from socket import socket, AF_INET, SOCK_STREAM

class Server(object):
    def __init__(self):
        self.message = ''

    def config_listening(self, server_port):
        '''
        Input:
            server_port: int, 80 for http
        '''
        self.socket_listening = socket(AF_INET, SOCK_STREAM)
        self.socket_listening.bind(('', server_port))
        self.socket_listening.listen(10)
        self.socket_listening.settimeout(1)
        print("The server is ready to receive")
        return

    def listen_to_connection(self):
        try:
            self.conn_socket, self.client_address = self.socket_listening.accept()
            print("Connection established with ", self.client_address)
        except:
            pass
        return
    
    def receive_once(self):
        try:
            self.listen_to_connection()
            message = self.conn_socket.recv(1024).decode().split('\n')[-1]
            print("Message received from %s: %s" % (self.client_address, self.message))
            self.conn_socket.close()
            return message
        except:
            return ''
        
