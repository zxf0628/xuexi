from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super(AddDialog, self).__init__(parent=parent)
        self.setWindowTitle("添加数据")
        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)


    def setupUI(self):
        self.student_id_Field = QLineEdit()
        self.student_id_Field.setObjectName("学号")
        self.name_Field = QLineEdit()
        self.name_Field.setObjectName("姓名")
        self.sex_Field = QLineEdit()
        self.sex_Field.setObjectName("性别")
        self.age_Field = QLineEdit()
        self.age_Field.setObjectName("年龄")
        self.grade_Field = QLineEdit()
        self.grade_Field.setObjectName("年级")

        layout = QFormLayout()
        layout.addRow("学号:", self.student_id_Field)
        layout.addRow("姓名:", self.name_Field)
        layout.addRow("性别:", self.sex_Field)
        layout.addRow("年龄:", self.age_Field)
        layout.addRow("年级:", self.grade_Field)
        self.global_layout.addLayout(layout)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.global_layout.addWidget(self.buttonsBox)
