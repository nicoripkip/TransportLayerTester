import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from socket_view import SocketView


APP_WIDTH   = 1280
APP_HEIGHT  = 720
APP_TITLE   = "Transport Layer Tester"


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.socket_view = SocketView()

        self.setWindowTitle(APP_TITLE)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.socket_view)


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = App()
    widget.resize(APP_WIDTH, APP_HEIGHT)
    widget.show()

    sys.exit(app.exec_())


if "__main__" == __name__:
    main()