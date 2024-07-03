import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from MysqlV2.data_centers.data_transfer import Data_Center


class AddDialog(QDialog):
    def __init__(self):
        super(AddDialog, self).__init__()
        self.data_centre = Data_Center()
        self.column_name = self.data_centre.get_label_column_name()
        print("AddDialog->__init__->开始实例输入界面ui,根据 数据中心列名：{}".format(self.column_name))

    def setupUI(self):
        self.global_layout = QVBoxLayout()
        self.joint_control_layout = QHBoxLayout()
        self.set_Label()
        self.set_LineEdit()
        self.global_layout.addLayout(self.joint_control_layout)
        self.set_butbox()
        self.setLayout(self.global_layout)

    def set_LineEdit(self):
        R_layout = QVBoxLayout()
        for i in range(len(self.column_name)):
            column_name = self.column_name[i]
            print("AddDialog->set_LineEdit->列名：{}".format(column_name))
            line_edit = QLineEdit()
            line_edit.setObjectName(column_name)
            R_layout.addWidget(line_edit)
        self.joint_control_layout.addLayout(R_layout)

    def set_Label(self):
        l_layout = QVBoxLayout()
        for i in range(len(self.column_name)):
            column_name = self.column_name[i]
            line_edit = QLabel(column_name)
            l_layout.addWidget(line_edit)
        self.joint_control_layout.addLayout(l_layout)

    def set_butbox(self):
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonsBox.rejected.connect(self.reject)
        self.global_layout.addWidget(self.buttonsBox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    zxf = AddDialog()
    zxf.show()
    sys.exit(app.exec_())
