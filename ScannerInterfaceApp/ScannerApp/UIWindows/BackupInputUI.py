# Form implementation generated from reading ui file 'UI_Files/BackupInputUI.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_BackupFileInput(object):
    def setupUi(self, BackupFileInput):
        BackupFileInput.setObjectName("BackupFileInput")
        BackupFileInput.resize(500, 150)
        BackupFileInput.setMaximumSize(QtCore.QSize(500, 150))
        font = QtGui.QFont()
        font.setPointSize(12)
        BackupFileInput.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(BackupFileInput)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(parent=BackupFileInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.input = QtWidgets.QLineEdit(parent=self.groupBox)
        self.input.setObjectName("input")
        self.gridLayout_2.addWidget(self.input, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=self.groupBox)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=BackupFileInput)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(BackupFileInput)
        self.buttonBox.accepted.connect(BackupFileInput.accept) # type: ignore
        self.buttonBox.rejected.connect(BackupFileInput.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(BackupFileInput)

    def retranslateUi(self, BackupFileInput):
        _translate = QtCore.QCoreApplication.translate
        BackupFileInput.setWindowTitle(_translate("BackupFileInput", "Dialog"))
        self.label.setText(_translate("BackupFileInput", "Enter Target Backup File Name:"))