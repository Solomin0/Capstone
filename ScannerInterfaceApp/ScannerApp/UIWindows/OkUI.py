# Form implementation generated from reading ui file 'ScannerApp/UI_Files/OkUI.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

'''
THIS SOFTWARE, ITS SOURCE CODE, AND ANY DISTRIBUTIONS THEREOF IS PROPERTY OF GEORGE MASON UNIVERSITY.
AUTHOR : MARTIN HAYNESWORTH
'''

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogOk(object):
    def setupUi(self, DialogOk):
        DialogOk.setObjectName("DialogOk")
        DialogOk.resize(210, 132)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        DialogOk.setFont(font)
        self.gridLayout_2 = QtWidgets.QGridLayout(DialogOk)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(parent=DialogOk)
        self.widget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=DialogOk)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(DialogOk)
        self.pushButton.clicked.connect(DialogOk.accept) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogOk)

    def retranslateUi(self, DialogOk):
        _translate = QtCore.QCoreApplication.translate
        DialogOk.setWindowTitle(_translate("DialogOk", "Dialog"))
        self.pushButton.setText(_translate("DialogOk", "Ok"))
        self.label.setText(_translate("DialogOk", "TextLabel"))
