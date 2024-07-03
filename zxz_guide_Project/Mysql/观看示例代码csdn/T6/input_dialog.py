# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_input(object):
    def setupUi(self, Dialog_input):
        Dialog_input.setObjectName("Dialog_input")
        Dialog_input.resize(394, 414)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_input)
        self.buttonBox.setGeometry(QtCore.QRect(-20, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.label = QtWidgets.QLabel(Dialog_input)
        self.label.setGeometry(QtCore.QRect(60, 110, 81, 18))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog_input)
        self.label_2.setGeometry(QtCore.QRect(60, 40, 81, 18))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog_input)
        self.label_3.setGeometry(QtCore.QRect(60, 180, 81, 18))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Dialog_input)
        self.label_4.setGeometry(QtCore.QRect(60, 240, 81, 18))
        self.label_4.setObjectName("label_4")

        self.line_name = QtWidgets.QLineEdit(Dialog_input)
        self.line_name.setGeometry(QtCore.QRect(130, 100, 181, 31))
        self.line_name.setObjectName("line_name")

        self.line_id = QtWidgets.QLineEdit(Dialog_input)
        self.line_id.setGeometry(QtCore.QRect(130, 30, 181, 31))
        self.line_id.setObjectName("line_id")

        self.line_sex = QtWidgets.QLineEdit(Dialog_input)
        self.line_sex.setGeometry(QtCore.QRect(130, 170, 181, 31))
        self.line_sex.setObjectName("line_sex")

        self.line_address = QtWidgets.QLineEdit(Dialog_input)
        self.line_address.setGeometry(QtCore.QRect(130, 240, 181, 31))
        self.line_address.setObjectName("line_address")

        self.retranslateUi(Dialog_input)
        self.buttonBox.rejected.connect(Dialog_input.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_input)
        Dialog_input.setTabOrder(self.line_id, self.line_name)
        Dialog_input.setTabOrder(self.line_name, self.line_sex)
        Dialog_input.setTabOrder(self.line_sex, self.line_address)

    def retranslateUi(self, Dialog_input):
        _translate = QtCore.QCoreApplication.translate
        Dialog_input.setWindowTitle(_translate("Dialog_input", "输入学生信息"))
        self.label.setText(_translate("Dialog_input", "姓名*："))
        self.label_2.setText(_translate("Dialog_input", "学号*："))
        self.label_3.setText(_translate("Dialog_input", "性别："))
        self.label_4.setText(_translate("Dialog_input", "籍贯："))
