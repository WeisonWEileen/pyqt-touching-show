# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\fpga\usb_cap8x8_v1\lib\ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1795, 872)
        font = QtGui.QFont()
        font.setBold(False)
        Form.setFont(font)
        Form.setAutoFillBackground(False)
        self.formGroupBox = QtWidgets.QGroupBox(Form)
        self.formGroupBox.setGeometry(QtCore.QRect(10, 90, 341, 161))
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.open_button = QtWidgets.QPushButton(self.formGroupBox)
        self.open_button.setObjectName("open_button")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.open_button)
        self.close_button = QtWidgets.QPushButton(self.formGroupBox)
        self.close_button.setObjectName("close_button")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.close_button)
        self.verticalGroupBox = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox.setGeometry(QtCore.QRect(390, 80, 851, 631))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.verticalGroupBox.setFont(font)
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_graph = QtWidgets.QVBoxLayout()
        self.verticalLayout_graph.setObjectName("verticalLayout_graph")
        self.verticalLayout.addLayout(self.verticalLayout_graph)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(80, 290, 171, 151))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 50, 171, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.quit_Button = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.quit_Button.sizePolicy().hasHeightForWidth())
        self.quit_Button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.quit_Button.setFont(font)
        self.quit_Button.setObjectName("quit_Button")
        self.gridLayout.addWidget(self.quit_Button, 1, 0, 1, 2)
        self.start_measure_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.start_measure_button.sizePolicy().hasHeightForWidth())
        self.start_measure_button.setSizePolicy(sizePolicy)
        self.start_measure_button.setObjectName("start_measure_button")
        self.gridLayout.addWidget(self.start_measure_button, 0, 0, 1, 2)
        self.savedata_button = QtWidgets.QPushButton(self.groupBox)
        self.savedata_button.setGeometry(QtCore.QRect(0, 0, 171, 51))
        self.savedata_button.setObjectName("savedata_button")
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setGeometry(QtCore.QRect(0, 450, 331, 401))
        self.groupBox_4.setObjectName("groupBox_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser.setGeometry(QtCore.QRect(110, 60, 211, 61))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setGeometry(QtCore.QRect(30, 90, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(30, 150, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(30, 230, 61, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(30, 300, 71, 16))
        self.label_4.setObjectName("label_4")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser_2.setGeometry(QtCore.QRect(110, 130, 211, 61))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser_3.setGeometry(QtCore.QRect(110, 210, 211, 61))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser_4.setGeometry(QtCore.QRect(110, 280, 211, 61))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.verticalGroupBox_2 = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox_2.setGeometry(QtCore.QRect(1370, 90, 271, 271))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.verticalGroupBox_2.setFont(font)
        self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_graph_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_graph_2.setObjectName("verticalLayout_graph_2")
        self.verticalLayout_2.addLayout(self.verticalLayout_graph_2)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(1440, 510, 2, 2))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_graph_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_graph_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_graph_3.setObjectName("verticalLayout_graph_3")
        self.verticalGroupBox_3 = QtWidgets.QGroupBox(Form)
        self.verticalGroupBox_3.setGeometry(QtCore.QRect(1370, 400, 271, 271))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.verticalGroupBox_3.setFont(font)
        self.verticalGroupBox_3.setObjectName("verticalGroupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalGroupBox_3)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_graph_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_graph_4.setObjectName("verticalLayout_graph_4")
        self.verticalLayout_3.addLayout(self.verticalLayout_graph_4)
        self.verticalGroupBox.raise_()
        self.formGroupBox.raise_()
        self.groupBox.raise_()
        self.groupBox_4.raise_()
        self.verticalGroupBox_2.raise_()
        self.layoutWidget.raise_()
        self.verticalGroupBox_3.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.open_button, self.close_button)
        Form.setTabOrder(self.close_button, self.savedata_button)
        Form.setTabOrder(self.savedata_button, self.textBrowser)
        Form.setTabOrder(self.textBrowser, self.textBrowser_2)
        Form.setTabOrder(self.textBrowser_2, self.textBrowser_3)
        Form.setTabOrder(self.textBrowser_3, self.textBrowser_4)
        Form.setTabOrder(self.textBrowser_4, self.quit_Button)
        Form.setTabOrder(self.quit_Button, self.start_measure_button)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "LZ数据系统"))
        self.formGroupBox.setTitle(_translate("Form", "启动设置"))
        self.open_button.setText(_translate("Form", "开始检测"))
        self.close_button.setText(_translate("Form", "停止检测"))
        self.verticalGroupBox.setTitle(_translate("Form", "动态显示窗口"))
        self.quit_Button.setText(_translate("Form", "退出"))
        self.start_measure_button.setText(_translate("Form", "清空"))
        self.savedata_button.setText(_translate("Form", "保存数据"))
        self.groupBox_4.setTitle(_translate("Form", "接收状态"))
        self.label.setText(_translate("Form", "DATA0"))
        self.label_2.setText(_translate("Form", "DATA1"))
        self.label_3.setText(_translate("Form", "DATA2"))
        self.label_4.setText(_translate("Form", "DATA3"))
        self.verticalGroupBox_2.setTitle(_translate("Form", "高度 prediction visualizaiton"))
        self.verticalGroupBox_3.setTitle(_translate("Form", "xy touch point visualizaiton"))
