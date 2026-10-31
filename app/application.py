import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


class PixVaultApplication:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.window = None

    def start(self):

        self.window = MainWindow()
        self.window.show()

        return self.qt_app.exec()
