from sys import argv
from PyQt6 import QtWidgets
from UIWindows import MainWindow


def boot() -> int:
    '''Start the application'''
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.show()
    code = app.exec()
    return code

if __name__ == '__main__':
    boot()    