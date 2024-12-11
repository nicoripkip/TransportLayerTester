import socket
import ssl
import threading
import config


class TCPBase:
    def __init__(self, ip: str, port: int, max_retries):
        """
        Constructor
        :param ip:
        :param port:
        :param max_retries:
        """
        self._socket = None
        self._tls_enabled = False
        self._ip = ip
        self._port = port
        self._max_retries = max_retries
        self._retries = 0


class TCPServer(TCPBase):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port, config.TCP_MAX_RETRIES)
        pass


class TCPClient(TCPBase):
    def __init__(self, ip: str, port: int):
        """
        Constructor
        :param ip:
        :param port:
        :param max_retries:
        """
        super().__init__(ip, port, config.TCP_MAX_RETRIES)
        self._connected = False
        self.construct()


    def construct(self):
        """
        Method
        :return:
        """
        if self._tls_enabled:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tls_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            # self.tls_ctx.load_verify_locations()
            self.tls_ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            self.tls_ctx.check_hostname = False
            self.tls_ctx.verify_mode = ssl.CERT_NONE
            self._socket = self.tls_ctx.wrap_socket(self.s, server_hostname=self._ip, server_side=False)
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self):
        """
        Method to connect to the server
        :return:
        """
        self._socket.connect((self._ip, self._port))
        self._connected = True


    def send(self, buff: str):
        """
        Method to send data to the client
        :param buff:
        :return:
        """
        self._socket.send(buff.encode())


    def recv(self):
        """
        Method to receive data from the client
        :return: str
        """
        return self._socket.recv(config.RECV_BUFFER_SIZE).decode()


    def get_connected(self):
        return self._connected


    def get_enable_tls(self):
        return self._tls_enabled


    def set_enable_tls(self, enable: bool):
        self._tls_enabled = enable
