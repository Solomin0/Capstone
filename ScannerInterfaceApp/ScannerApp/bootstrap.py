'''
THIS SOFTWARE, ITS SOURCE CODE, AND ANY DISTRIBUTIONS THEREOF IS PROPERTY OF GEORGE MASON UNIVERSITY.
AUTHOR : MARTIN HAYNESWORTH
'''

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