from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainUi(QWidget):
    def __init__(self):
        super(MainUi, self).__init__()

    # ui界面拼接
    def join_ui(self):
        self.right_ui()
        self.global_layout = QHBoxLayout()

        self.tableWidget = QTableWidget()
        self.global_layout.addWidget(self.tableWidget)
        self.global_layout.addLayout(self.right_layout)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def set_show_ui(self):
        self.join_ui()
        self.setLayout(self.global_layout)
        self.setFixedSize(QSize(600, 400))
        self.setWindowTitle('查询数据库')

    def right_ui(self):
        self.right_layout = QVBoxLayout()
        self.init_row1()
        self.init_row2()
        self.init_row3()
        self.init_row4()
        self.init_row5_select()
        self.init_row7_delete()
        self.init_row11_to_load_data()
        self.init_row8_insert()
        self.init_row6_save()
        self.init_row10_close()
        self.init_row9_statusBar()

    def set_ui_control_size(self, control, length=80, wide=30):
        control.setFixedSize(QSize(int(length), int(wide)))

    def init_row1(self):
        self.button_open_databases = QPushButton("打开mysql数据库")
        self.button_show_databases_name = QPushButton("显示库名")

        self.right_layout.addWidget(self.button_open_databases)
        self.right_layout.addWidget(self.button_show_databases_name)

    def init_row2(self):
        self.comboBox_select_databases = QComboBox()
        self.button_select_databases = QPushButton("选择此数据库")
        self.set_ui_control_size(self.button_select_databases)

        row2 = QHBoxLayout()
        row2.addWidget(self.comboBox_select_databases)
        row2.addWidget(self.button_select_databases)
        self.right_layout.addLayout(row2)

    def init_row3(self):
        self.comboBox_select_datatable = QComboBox()
        self.button_select_datatable = QPushButton("选择此数据表")
        self.set_ui_control_size(self.button_select_datatable)

        row3 = QHBoxLayout()
        row3.addWidget(self.comboBox_select_datatable)
        row3.addWidget(self.button_select_datatable)
        self.right_layout.addLayout(row3)

    def init_row4(self):
        self.LineEdit_label_column_name = QLineEdit()
        self.LineEdit_label_column_name.setReadOnly(True)
        self.Label_label_column_name = QLabel("列名展示：")

        row4 = QHBoxLayout()
        row4.addWidget(self.Label_label_column_name)
        row4.addWidget(self.LineEdit_label_column_name)
        self.right_layout.addLayout(row4)

    def init_row5_select(self):
        self.ComboBox_select_condition_name = QComboBox()
        self.ComboBox_select_condition_operator = QComboBox()
        self.LineEdit_select_condition = QLineEdit()
        self.LineEdit_select_condition.setPlaceholderText("条件")
        self.button_select_condition = QPushButton("查询数据")

        row5 = QHBoxLayout()
        row5.addWidget(self.ComboBox_select_condition_name)
        row5.addWidget(QLabel(":"))
        row5.addWidget(self.ComboBox_select_condition_operator)
        row5.addWidget(QLabel(":"))
        row5.addWidget(self.LineEdit_select_condition)
        row5.addWidget(self.button_select_condition)
        self.right_layout.addLayout(row5)

    def init_row6_save(self):
        self.button_save_data = QPushButton("保存数据")
        self.button_save_data.setEnabled(False)

        row6 = QHBoxLayout()
        row6.addWidget(self.button_save_data)
        self.right_layout.addLayout(row6)

    def init_row7_delete(self):
        self.ComboBox_delete_where_name = QComboBox()
        self.ComboBox_delete_where_operator = QComboBox()
        self.LineEdit_delete_where = QLineEdit()
        self.LineEdit_delete_where.setPlaceholderText("条件")
        self.button_delete_data = QPushButton("删除数据")

        row7 = QHBoxLayout()
        row7.addWidget(self.ComboBox_delete_where_name)
        row7.addWidget(QLabel(":"))
        row7.addWidget(self.ComboBox_delete_where_operator)
        row7.addWidget(QLabel(":"))
        row7.addWidget(self.LineEdit_delete_where)
        row7.addWidget(self.button_delete_data)
        self.right_layout.addLayout(row7)

    def init_row8_insert(self):
        self.button_insert_data = QPushButton("添加数据")

        row8 = QHBoxLayout()
        row8.addWidget(self.button_insert_data)
        self.right_layout.addLayout(row8)

    def init_row9_statusBar(self):
        self.statusBar = QStatusBar()
        self.set_ui_control_size(self.statusBar, 200, 40)
        self.right_layout.addWidget(self.statusBar)

    def init_row10_close(self):
        self.button_close = QPushButton("关闭数据连接")

        self.right_layout.addWidget(self.button_close)

    def init_row11_to_load_data(self):
        self.button_to_load_data = QPushButton("加载数据")
        self.right_layout.addWidget(self.button_to_load_data)


