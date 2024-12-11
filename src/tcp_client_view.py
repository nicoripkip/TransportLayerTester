from PySide6 import QtCore, QtWidgets
from tcp import TCPClient
from buffers import MessageBuffer, MsgObject, ThreadBuffer
import threading


FIXED_WIDGET_WIDTH = 130
FIXED_WIDGET_HEIGHT = 20


class SocketView(QtWidgets.QWidget):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        self.tcp_client = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_text_browser)
        self.timer.start(1)

        self.layout         = QtWidgets.QHBoxLayout(self)
        self.layout_left    = QtWidgets.QVBoxLayout()
        self.layout_right   = QtWidgets.QVBoxLayout()
        self.layout_mod     = QtWidgets.QVBoxLayout()
        self.layout_send    = QtWidgets.QHBoxLayout()

        self.ip_address     = ""
        self.ip_port        = ""

        # Setup internal messaging system for receiving data from threads
        self.buffer = MessageBuffer()
        self.message = ""

        self.thread_buffer = ThreadBuffer()
        self.thread_counter = 0

        # Try to subscribe
        self.buffer.subscribe("tcpclient", "gui", self.update_buffer)

        self.draw()


    def draw(self):
        """
        Method to draw the frontend page
        :return: None
        """
        self.text_browser = QtWidgets.QTextBrowser()

        # These stuf are for filling the ip address
        self.label_ip   = QtWidgets.QLabel("Ip address:")
        self.label_ip.setFixedWidth(FIXED_WIDGET_WIDTH)
        self.label_ip.setFixedHeight(FIXED_WIDGET_HEIGHT)
        self.label_ip.setStyleSheet("background-color: #FFFFFF; color: #000000;")

        self.label_port = QtWidgets.QLabel("Port: ")
        self.label_port.setFixedWidth(FIXED_WIDGET_WIDTH)
        self.label_port.setFixedHeight(FIXED_WIDGET_HEIGHT)
        self.label_port.setStyleSheet("background-color: #FFFFFF; color: #000000;")

        self.input_ip   = QtWidgets.QLineEdit()
        self.input_ip.setPlaceholderText("Type here....")
        self.input_ip.setFixedWidth(FIXED_WIDGET_WIDTH)
        self.input_ip.setFixedHeight(FIXED_WIDGET_HEIGHT)

        self.input_port   = QtWidgets.QLineEdit()
        self.input_port.setPlaceholderText("Type here....")
        self.input_port.setFixedWidth(FIXED_WIDGET_WIDTH)
        self.input_port.setFixedHeight(FIXED_WIDGET_HEIGHT)
        self.input_port.setMaxLength(6)
        
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_socket)

        self.ping_button = QtWidgets.QPushButton("Ping")
        self.ping_button.clicked.connect(self.ping_to_socket)

        self.ip_left = QtWidgets.QVBoxLayout()
        self.ip_right = QtWidgets.QVBoxLayout()

        self.ip_ver = QtWidgets.QHBoxLayout()
        self.ip_ver.addLayout(self.ip_left)
        self.ip_ver.addLayout(self.ip_right)

        self.ip_left.addWidget(self.label_ip)
        self.ip_left.addWidget(self.input_ip)
        self.ip_left.addWidget(self.ping_button)
        self.ip_right.addWidget(self.label_port)
        self.ip_right.addWidget(self.input_port)
        self.ip_right.addWidget(self.connect_button)

        self.group_ip = QtWidgets.QGroupBox("TCP")
        self.group_ip.setFixedWidth(300)
        self.group_ip.setFixedHeight(150)
        self.group_ip.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.group_ip.setLayout(self.ip_ver)

        # TLS Options
        self.tls_cert_label = QtWidgets.QLabel("TLS Certificate:")
        self.tls_cert_label.setFixedWidth(FIXED_WIDGET_WIDTH)
        self.tls_cert_label.setFixedHeight(FIXED_WIDGET_HEIGHT)
        self.tls_cert_label.setStyleSheet("background-color: #FFFFFF; color: #000000;")

        self.tls_key_label = QtWidgets.QLabel("TLS Key:")
        self.tls_key_label.setFixedWidth(FIXED_WIDGET_WIDTH)
        self.tls_key_label.setFixedHeight(FIXED_WIDGET_HEIGHT)
        self.tls_key_label.setStyleSheet("background-color: #FFFFFF; color: #000000;")

        self.tls_cert_file = QtWidgets.QFileDialog()
        self.tls_cert_file.setFixedWidth(FIXED_WIDGET_WIDTH)
        self.tls_cert_file.setFixedHeight(FIXED_WIDGET_HEIGHT)

        self.tls_left = QtWidgets.QVBoxLayout()
        self.tls_right = QtWidgets.QVBoxLayout()
        self.tls_ver = QtWidgets.QHBoxLayout()
        self.tls_ver.addLayout(self.tls_left)
        self.tls_ver.addLayout(self.tls_right)

        self.tls_left.addWidget(self.tls_cert_label)
        self.tls_left.addWidget(self.tls_cert_file)
        self.tls_right.addWidget(self.tls_key_label)

        self.group_TLS = QtWidgets.QGroupBox("TLS")
        self.group_TLS.setFixedWidth(300)
        self.group_TLS.setFixedHeight(150)
        self.group_TLS.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.group_TLS.setLayout(self.tls_ver)

        # Connections options
        self.group_connections = QtWidgets.QGroupBox("Connections")
        self.group_connections.setFixedWidth(300)
        self.group_connections.setFixedHeight(200)
        self.group_connections.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # These stuff is for handling send data


        self.input_send = QtWidgets.QLineEdit()
        self.input_send.setPlaceholderText("Type here....")
        self.input_send.setFixedHeight(40)

        self.button_send = QtWidgets.QPushButton("Send")
        self.button_send.clicked.connect(self.send_to_socket)

        self.layout_send.addWidget(self.input_send)
        self.layout_send.addWidget(self.button_send)

        # add the text browser
        self.layout_left.addWidget(self.text_browser)
        self.layout_left.addLayout(self.layout_send)

        # Add the rest of the layouts
        self.layout_mod.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_mod.addWidget(self.group_ip)
        self.layout_mod.addWidget(self.group_TLS)
        self.layout_mod.addWidget(self.group_connections)

        self.layout_right.addLayout(self.layout_mod)

        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)


    def update_text_browser(self):
        """
        Update method for updating the textbox
        :return: None
        """
        # Update the contents of the
        if len(self.message) > 0:
            # self.text_browser.clear()
            self.text_browser.append(self.message)
            self.message = ""


    def connect_to_socket(self):
        """
        Method to setup threads for connecting to a TCP Server
        :return:
        """
        if len(self.input_ip.text()) == 0:
            return

        if len(self.input_port.text()) == 0:
            return

        self.ip_address = self.input_ip.text()
        self.ip_port    = int(self.input_port.text())

        self.buffer.publish("tcpclient", f"Trying to connect to: {self.ip_address}:{self.ip_port}")

        t = threading.Thread(target=self.tcp_worker, args=(self.ip_address, self.ip_port, f"tcp_client_{self.thread_counter}"))
        t.start()

        self.thread_buffer.add_thread(f"tcp_client_{self.thread_counter}", t)

        self.thread_counter += 1


    def send_to_socket(self):
        """
        This method is gonna send data to the socket
        :return:
        """
        pass


    def ping_to_socket(self):
        """
        Method to ping the socket to check if the socket is online
        :return: None
        """
        if len(self.input_ip.text()) == 0:
            return

        if len(self.input_port.text()) == 0:
            return

        self.ip_address = self.input_ip.text()
        self.ip_port = int(self.input_port.text())


    def update_buffer(self, msg: str):
        """
        Callback method for receiving data from the message queue
        :param msg:
        :return: None
        """
        self.message = msg


    def tcp_worker(self, ip: str, port: int, thread_id: str):
        """
        Worker method which is gonna be used in the threads that this window is gonna spawn
        :param ip:
        :param port:
        :return: None
        """
        self.buffer.publish("tcpclient", f"thread: {thread_id} tries to connect to: {ip}:{port}")

        # Set up tcp server and try to connect to a given
        client = TCPClient(ip, port)
        client.set_enable_tls(False)
        client.connect()

        # Abort thread if not connected
        if not client.get_connected():
            self.buffer.publish("tcpclient", f"thread: {thread_id} failed to connect to: {ip}:{port}")
            return

        self.buffer.publish("tcpclient", f"thread: {thread_id} is succesfully connected to: {ip}:{port}")

        # Run the client
        while client.get_connected():
            # data = client.recv()
            # self.buffer.publish("tcpclient", data)
            pass