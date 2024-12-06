from PySide6 import QtCore, QtWidgets
from tcp import TCPClient
from buffers import MessageBuffer, MessageObject
import threading


FIXED_WIDGET_WIDTH = 130
FIXED_WIDGET_HEIGHT = 20


class SocketView(QtWidgets.QWidget):
    _message = None

    def __init__(self):
        super().__init__()

        self.tcp_client = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_text_browser)
        self.timer.start(100)

        self.layout         = QtWidgets.QHBoxLayout(self)
        self.layout_left    = QtWidgets.QVBoxLayout()
        self.layout_right   = QtWidgets.QVBoxLayout()
        self.layout_mod     = QtWidgets.QVBoxLayout()
        self.layout_send    = QtWidgets.QHBoxLayout()

        self.ip_address     = ""
        self.ip_port        = ""
        self.message_buff = MessageBuffer()

        self.buffer = []

        self.draw()


    def draw(self):
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
        # Update the contents of the textbrowser
        self.text_browser.clear()
        self.text_browser.append("\n".join(self.buffer))

    def connect_to_socket(self):
        self.ip_address = self.input_ip.text()
        self.ip_port    = int(self.input_port.text())

        self.buffer.append(f"Trying to connect to: {self.ip_address}:{self.ip_port}")

        if len(self.ip_address) > 0:
            print(self.ip_address)

        if self.ip_port > 0:
            print(self.ip_port)

        # self.tcp_client = TCPClient(self.ip_address, self.ip_port)
        # self.tcp_client.connect()


    def send_to_socket(self):
        pass


    def ping_to_socket(self):
        self.buffer.append("Trying to ping: ")
