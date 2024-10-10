import socket


class TCPSocket:
    def __init__(self, ip, port):
        self.socket = None
    

    def construct(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        pass
        

    def send(self):
        pass       


    def recv(self):
        pass