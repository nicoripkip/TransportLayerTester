from PySide6 import QtCore, QtWidgets, QtGui


FIXED_WIDTH = 350


class SocketView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout         = QtWidgets.QHBoxLayout(self)
        self.layout_left    = QtWidgets.QVBoxLayout()
        self.layout_right   = QtWidgets.QVBoxLayout()
        self.layout_mod     = QtWidgets.QVBoxLayout()
        self.layout_send    = QtWidgets.QHBoxLayout()

        self.ip_address     = ""
        self.ip_port        = ""

        self.draw()


    def draw(self):
        label2 = QtWidgets.QTextBrowser()
        #label2.setFixedWidth(1000)
        
        label3 = QtWidgets.QLabel("Testlabel3")
        #label3.setFixedWidth(1000)
        label3.setFixedHeight(170)

        self.label_ip   = QtWidgets.QLabel("Ip address:")
        self.label_ip.setFixedWidth(FIXED_WIDTH)
        self.label_ip.setFixedHeight(20)
        self.label_ip.setStyleSheet("background-color: #FFFFFF; color: #000000;")

        self.label_port = QtWidgets.QLabel("Port: ")
        self.label_port.setFixedWidth(FIXED_WIDTH)
        self.label_port.setFixedHeight(20)
        self.label_port.setStyleSheet("background-color: #FFFFFF; color: #000000;")

        self.input_ip   = QtWidgets.QLineEdit()
        self.input_ip.setPlaceholderText("Type here....")
        self.input_ip.setFixedWidth(FIXED_WIDTH)
        self.input_ip.setFixedHeight(20)    

        self.input_port   = QtWidgets.QLineEdit()
        self.input_port.setPlaceholderText("Type here....")
        self.input_port.setFixedWidth(FIXED_WIDTH)
        self.input_port.setFixedHeight(20)    
        self.input_port.setMaxLength(6)    
        
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_socket)

        self.input_send = QtWidgets.QLineEdit()
        self.input_send.setPlaceholderText("Type here....")
        self.input_send.setFixedHeight(40)

        self.button_send = QtWidgets.QPushButton("Send")
        self.button_send.clicked.connect(self.send_to_socket)

        self.layout_send.addWidget(self.input_send)
        self.layout_send.addWidget(self.button_send)

        self.layout_left.addWidget(label2)
        self.layout_left.addLayout(self.layout_send)

        self.layout_mod.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_mod.addWidget(self.label_ip)
        self.layout_mod.addWidget(self.input_ip)
        self.layout_mod.addWidget(self.label_port)
        self.layout_mod.addWidget(self.input_port)
        self.layout_mod.addWidget(self.connect_button)
        
        self.layout_right.addLayout(self.layout_mod)

        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)


    def connect_to_socket(self):
        self.ip_address = self.input_ip.text()
        self.ip_port    = self.input_port.text()

        if len(self.ip_address) > 0:
            print(self.ip_address)

        if len(self.ip_port) > 0:
            print(self.ip_port)


    def send_to_socket(self):
        pass