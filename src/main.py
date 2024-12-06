import sys
from PySide6 import QtWidgets
from socket_view import SocketView
import threading
import config
from src.buffers import ThreadBuffer

APP_TITLE   = "Transport Layer Tester"


thread_buffer = ThreadBuffer()


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.socket_view = SocketView()

        self.tabular = QtWidgets.QTabWidget()
        self.tabular.addTab(self.socket_view, "TCP Client")
        self.tabular.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle(APP_TITLE)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.tabular)


def run_app():
    print("Thread: [GUI] Started.")
    app = QtWidgets.QApplication(sys.argv)

    widget = App()
    widget.resize(config.APP_WIDTH, config.APP_HEIGHT)
    widget.show()

    sys.exit(app.exec())
    # print("Thread: [GUI] Ended.")


def main():
    t1 = threading.Thread(target=run_app)

    thread_buffer.add_thread("gui", t1)

    t1.start()

    t1.join()

if "__main__" == __name__:
    main()