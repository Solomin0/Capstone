from PyQt6 import QtWidgets
from sys import argv
from UIWindows import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()