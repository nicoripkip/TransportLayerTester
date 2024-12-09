import socket
import ssl
import threading


class TCPBase:
    def __init__(self):
        pass


class TCPServer(TCPBase):
    def __init__(self):
        super.__init__()
        pass


class TCPClient:
    def __init__(self, ip: str, port: int):
        self.socket = None
        self.connected = False
        self.tls_enabled = False
        self.ip = ip
        self.port = port
        self.retries = 0

        self.construct()

    def construct(self):
        if self.tls_enabled:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tls_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            # self.tls_ctx.load_verify_locations()
            self.tls_ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            self.tls_ctx.check_hostname = False
            self.tls_ctx.verify_mode = ssl.CERT_NONE
            self.socket = self.tls_ctx.wrap_socket(self.s, server_hostname=self.ip, server_side=False)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.ip, self.port))
        self.connected = True

    def send(self):
        pass       

    def recv(self):
        pass

    def get_connected(self):
        return self.connected

    def get_enable_tls(self):
        return self.tls_enabled

    def set_enable_tls(self, enable: bool):
        self.tls_enabled = enable
