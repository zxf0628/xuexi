# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_info(object):
    def setupUi(self, Dialog_info):
        Dialog_info.setObjectName("Dialog_info")
        Dialog_info.resize(465, 349)
        self.button_confirm = QtWidgets.QPushButton(Dialog_info)
        self.button_confirm.setGeometry(QtCore.QRect(300, 300, 112, 34))
        self.button_confirm.setObjectName("button_confirm")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog_info)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 50, 331, 229))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        self.line_id = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.line_id.setObjectName("line_id")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_id)
        self.line_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.line_name.setObjectName("line_name")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.line_name)
        self.line_sex = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.line_sex.setObjectName("line_sex")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.line_sex)
        self.line_address = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.line_address.setObjectName("line_address")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.line_address)

        self.retranslateUi(Dialog_info)
        QtCore.QMetaObject.connectSlotsByName(Dialog_info)
        Dialog_info.setTabOrder(self.line_id, self.line_name)
        Dialog_info.setTabOrder(self.line_name, self.line_sex)
        Dialog_info.setTabOrder(self.line_sex, self.line_address)
        Dialog_info.setTabOrder(self.line_address, self.button_confirm)

    def retranslateUi(self, Dialog_info):
        _translate = QtCore.QCoreApplication.translate
        Dialog_info.setWindowTitle(_translate("Dialog_info", "学生信息详情"))
        self.button_confirm.setText(_translate("Dialog_info", "确定"))
        self.label.setText(_translate("Dialog_info", "学号"))
        self.label_2.setText(_translate("Dialog_info", "姓名"))
        self.label_3.setText(_translate("Dialog_info", "性别"))
        self.label_4.setText(_translate("Dialog_info", "籍贯"))
