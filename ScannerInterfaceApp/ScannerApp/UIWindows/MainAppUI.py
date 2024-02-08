# Form implementation generated from reading ui file 'UI_Files/MainAppUI.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(629, 434)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.main_screen_stack = StackedWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_screen_stack.sizePolicy().hasHeightForWidth())
        self.main_screen_stack.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.main_screen_stack.setFont(font)
        self.main_screen_stack.setLineWidth(2)
        self.main_screen_stack.setMidLineWidth(2)
        self.main_screen_stack.setObjectName("main_screen_stack")
        self.main_menu = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.main_menu.setFont(font)
        self.main_menu.setObjectName("main_menu")
        self.gridLayout = QtWidgets.QGridLayout(self.main_menu)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.MainMenu = QtWidgets.QVBoxLayout()
        self.MainMenu.setContentsMargins(-1, 12, -1, -1)
        self.MainMenu.setSpacing(0)
        self.MainMenu.setObjectName("MainMenu")
        self.mm_header = QtWidgets.QLabel(parent=self.main_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mm_header.sizePolicy().hasHeightForWidth())
        self.mm_header.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.mm_header.setFont(font)
        self.mm_header.setScaledContents(False)
        self.mm_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mm_header.setObjectName("mm_header")
        self.MainMenu.addWidget(self.mm_header)
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.MainMenu.addItem(spacerItem)
        self.button_canvas = QtWidgets.QGroupBox(parent=self.main_menu)
        self.button_canvas.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.button_canvas.setFont(font)
        self.button_canvas.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.button_canvas.setAcceptDrops(False)
        self.button_canvas.setTitle("")
        self.button_canvas.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.button_canvas.setFlat(False)
        self.button_canvas.setCheckable(False)
        self.button_canvas.setObjectName("button_canvas")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.button_canvas)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mm_new_scan_btn = PushButton(parent=self.button_canvas)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mm_new_scan_btn.sizePolicy().hasHeightForWidth())
        self.mm_new_scan_btn.setSizePolicy(sizePolicy)
        self.mm_new_scan_btn.setObjectName("mm_new_scan_btn")
        self.verticalLayout.addWidget(self.mm_new_scan_btn)
        self.mm_view_scans_btn = PushButton(parent=self.button_canvas)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mm_view_scans_btn.sizePolicy().hasHeightForWidth())
        self.mm_view_scans_btn.setSizePolicy(sizePolicy)
        self.mm_view_scans_btn.setObjectName("mm_view_scans_btn")
        self.verticalLayout.addWidget(self.mm_view_scans_btn)
        self.mm_sync_db_btn = PushButton(parent=self.button_canvas)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mm_sync_db_btn.sizePolicy().hasHeightForWidth())
        self.mm_sync_db_btn.setSizePolicy(sizePolicy)
        self.mm_sync_db_btn.setObjectName("mm_sync_db_btn")
        self.verticalLayout.addWidget(self.mm_sync_db_btn)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        self.MainMenu.addWidget(self.button_canvas)
        self.gridLayout.addLayout(self.MainMenu, 0, 0, 1, 1)
        self.main_screen_stack.addWidget(self.main_menu)
        self.new_scan = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_scan.sizePolicy().hasHeightForWidth())
        self.new_scan.setSizePolicy(sizePolicy)
        self.new_scan.setObjectName("new_scan")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.new_scan)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.new_scan)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ns_submit_label = QtWidgets.QLabel(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ns_submit_label.sizePolicy().hasHeightForWidth())
        self.ns_submit_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setKerning(True)
        self.ns_submit_label.setFont(font)
        self.ns_submit_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ns_submit_label.setObjectName("ns_submit_label")
        self.verticalLayout_2.addWidget(self.ns_submit_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ns_serial_no = QtWidgets.QLineEdit(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ns_serial_no.sizePolicy().hasHeightForWidth())
        self.ns_serial_no.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.ns_serial_no.setFont(font)
        self.ns_serial_no.setObjectName("ns_serial_no")
        self.horizontalLayout.addWidget(self.ns_serial_no)
        self.ns_submit_btn = QtWidgets.QPushButton(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ns_submit_btn.sizePolicy().hasHeightForWidth())
        self.ns_submit_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.ns_submit_btn.setFont(font)
        self.ns_submit_btn.setObjectName("ns_submit_btn")
        self.horizontalLayout.addWidget(self.ns_submit_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 15, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ns_back_btn = PushButton(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ns_back_btn.sizePolicy().hasHeightForWidth())
        self.ns_back_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.ns_back_btn.setFont(font)
        self.ns_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ns_back_btn.setObjectName("ns_back_btn")
        self.horizontalLayout_3.addWidget(self.ns_back_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.main_screen_stack.addWidget(self.new_scan)
        self.view_scans = QtWidgets.QWidget()
        self.view_scans.setObjectName("view_scans")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.view_scans)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.vs_backup_btn = PushButton(parent=self.view_scans)
        self.vs_backup_btn.setObjectName("vs_backup_btn")
        self.horizontalLayout_5.addWidget(self.vs_backup_btn)
        self.vs_sync_db_btn = PushButton(parent=self.view_scans)
        self.vs_sync_db_btn.setObjectName("vs_sync_db_btn")
        self.horizontalLayout_5.addWidget(self.vs_sync_db_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.vs_add_row_btn = PushButton(parent=self.view_scans)
        self.vs_add_row_btn.setObjectName("vs_add_row_btn")
        self.horizontalLayout_5.addWidget(self.vs_add_row_btn)
        self.vs_new_scan_btn = PushButton(parent=self.view_scans)
        self.vs_new_scan_btn.setObjectName("vs_new_scan_btn")
        self.horizontalLayout_5.addWidget(self.vs_new_scan_btn)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.groupBox = QtWidgets.QGroupBox(parent=self.view_scans)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.vs_scans_table = Table(parent=self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setKerning(True)
        self.vs_scans_table.setFont(font)
        self.vs_scans_table.setObjectName("vs_scans_table")
        self.vs_scans_table.setColumnCount(5)
        self.vs_scans_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.vs_scans_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vs_scans_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vs_scans_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.vs_scans_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.vs_scans_table.setHorizontalHeaderItem(4, item)
        self.vs_scans_table.horizontalHeader().setStretchLastSection(False)
        self.gridLayout_2.addWidget(self.vs_scans_table, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.vs_reset_btn = PushButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vs_reset_btn.sizePolicy().hasHeightForWidth())
        self.vs_reset_btn.setSizePolicy(sizePolicy)
        self.vs_reset_btn.setObjectName("vs_reset_btn")
        self.horizontalLayout_2.addWidget(self.vs_reset_btn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.vs_to_mm_btn = PushButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vs_to_mm_btn.sizePolicy().hasHeightForWidth())
        self.vs_to_mm_btn.setSizePolicy(sizePolicy)
        self.vs_to_mm_btn.setObjectName("vs_to_mm_btn")
        self.horizontalLayout_2.addWidget(self.vs_to_mm_btn)
        self.vs_save_btn = PushButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vs_save_btn.sizePolicy().hasHeightForWidth())
        self.vs_save_btn.setSizePolicy(sizePolicy)
        self.vs_save_btn.setObjectName("vs_save_btn")
        self.horizontalLayout_2.addWidget(self.vs_save_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.vs_edit_area = QtWidgets.QVBoxLayout()
        self.vs_edit_area.setObjectName("vs_edit_area")
        self.gridLayout_2.addLayout(self.vs_edit_area, 2, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.main_screen_stack.addWidget(self.view_scans)
        self.gridLayout_4.addWidget(self.main_screen_stack, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = StatusBar(parent=MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionBackup_Scans = QtGui.QAction(parent=MainWindow)
        self.actionBackup_Scans.setObjectName("actionBackup_Scans")

        self.retranslateUi(MainWindow)
        self.main_screen_stack.setCurrentIndex(0)
        self.vs_scans_table.cellChanged['int','int'].connect(self.vs_scans_table.update_scans) # type: ignore
        self.vs_add_row_btn.clicked.connect(self.vs_scans_table.add_row) # type: ignore
        self.vs_save_btn.clicked.connect(self.vs_scans_table.try_save_changes) # type: ignore
        self.vs_reset_btn.clicked.connect(self.vs_scans_table.reset_table) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.mm_new_scan_btn, self.mm_sync_db_btn)
        MainWindow.setTabOrder(self.mm_sync_db_btn, self.mm_view_scans_btn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Asset Scanner"))
        self.mm_header.setText(_translate("MainWindow", "Asset Scanner"))
        self.mm_new_scan_btn.setText(_translate("MainWindow", "New Scan"))
        self.mm_view_scans_btn.setText(_translate("MainWindow", "View Scans"))
        self.mm_sync_db_btn.setText(_translate("MainWindow", "Sync Database"))
        self.ns_submit_label.setText(_translate("MainWindow", "Scan or Enter Serial Number:"))
        self.ns_submit_btn.setText(_translate("MainWindow", "Submit"))
        self.ns_back_btn.setText(_translate("MainWindow", "Back"))
        self.vs_backup_btn.setText(_translate("MainWindow", "Backup Scans"))
        self.vs_sync_db_btn.setText(_translate("MainWindow", "Sync Database"))
        self.vs_add_row_btn.setText(_translate("MainWindow", "Add Row"))
        self.vs_new_scan_btn.setText(_translate("MainWindow", "Scan"))
        self.groupBox.setTitle(_translate("MainWindow", "Current Scans"))
        item = self.vs_scans_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Serial_No"))
        item = self.vs_scans_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Short_Desc"))
        item = self.vs_scans_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Location"))
        item = self.vs_scans_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Timestamp"))
        item = self.vs_scans_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Price"))
        self.vs_reset_btn.setText(_translate("MainWindow", "Reset"))
        self.vs_to_mm_btn.setText(_translate("MainWindow", "Back"))
        self.vs_save_btn.setText(_translate("MainWindow", "Save"))
        self.actionBackup_Scans.setText(_translate("MainWindow", "Backup Scans"))
from .uielements import PushButton, StackedWidget, StatusBar, Table
