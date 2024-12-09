import sys
from PySide6 import QtWidgets
import time

from src.about_view import AboutView
from tcp_client_view import SocketView
import threading
import config
from buffers import ThreadBuffer, MessageBuffer


APP_TITLE   = "Transport Layer Tester"


thread_buffer = ThreadBuffer()
gui_closed = False



class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.socket_view = SocketView()
        self.about_view  = AboutView()

        self.tabular = QtWidgets.QTabWidget()
        self.tabular.addTab(self.socket_view, "TCP Client")
        self.tabular.addTab(self.about_view, "About")
        self.tabular.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle(APP_TITLE)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.tabular)

    def closeEvent(self, event):
        global gui_closed
        gui_closed = True


def run_app():
    print("Thread: [GUI] Started.")
    app = QtWidgets.QApplication(sys.argv)

    widget = App()
    widget.resize(config.APP_WIDTH, config.APP_HEIGHT)
    widget.show()

    sys.exit(app.exec())
    # print("Thread: [GUI] Ended.")


def run_broker():
    msg_buf = MessageBuffer()
    global gui_closed

    print("Thread: [Broker] Started.")

    if msg_buf.check_lock():
        pass

    while not gui_closed:
        msg_buf.poll()

    return


if "__main__" == __name__:
    t1 = threading.Thread(target=run_app)
    t2 = threading.Thread(target=run_broker)

    thread_buffer.add_thread("gui", t1)
    thread_buffer.add_thread("broker", t2)

    t2.start()
    t1.start()

    t1.join()
    t2.join()