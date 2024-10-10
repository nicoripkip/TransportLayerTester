import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


APP_WIDTH   = 1280
APP_HEIGHT  = 720
APP_TITLE   = "Transport Layer Tester"


class App(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        # Set window size
        self.setGeometry(100, 100, 600, 400)


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = App()
    widget.resize(APP_WIDTH, APP_HEIGHT)
    widget.show()

    sys.exit(app.exec_())


if "__main__" == __name__:
    main()