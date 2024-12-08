from PySide6 import QtCore, QtWidgets


class AboutView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout         = QtWidgets.QVBoxLayout(self)
        self.widget_top     = QtWidgets.QTextBrowser()
        self.widget_bottom  = QtWidgets.QWidget()

        self.draw()

    def draw(self):
        # Config widget Bottom
        self.widget_bottom.setFixedHeight(50)

        # Add the widgets
        self.layout.addWidget(self.widget_top)
        self.layout.addWidget(self.widget_bottom)
        self.layout.setContentsMargins(0, 0, 0, 0)