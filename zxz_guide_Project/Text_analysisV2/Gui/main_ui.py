from PyQt5.QtWidgets import *


def set_control_size(control, w=80, h=20):
    control.setFixedSize(w, h)


class Text_analysis_ui(QWidget):
    def __init__(self):
        super(Text_analysis_ui, self).__init__()

    def join_ui(self):
        self.global_layout = QVBoxLayout()

        self.init_row1()
        self.init_row2()
        self.init_row3()
        self.init_close_row()
        self.init_row4()

        self.statusBar = QStatusBar()
        self.global_layout.addWidget(self.statusBar)

    def show_ui(self):
        self.join_ui()
        self.setLayout(self.global_layout)
        self.setFixedSize(550, 400)
        self.setWindowTitle('读取LOG数据')

    def init_row1(self):
        self.ledit_file_path = QLineEdit()
        self.button_select_file = QPushButton("选择文件")
        set_control_size(self.button_select_file)

        row1 = QHBoxLayout()
        row1.addWidget(self.ledit_file_path)
        row1.addWidget(self.button_select_file)
        self.global_layout.addLayout(row1)

    def init_row3(self):
        self.ledit_row_mark = QLineEdit()
        self.ledit_row_mark.setPlaceholderText("行号")
        set_control_size(self.ledit_row_mark)

        self.ledit_col_mark = QLineEdit()
        self.ledit_col_mark.setPlaceholderText("列号")
        set_control_size(self.ledit_col_mark)

        self.button_get_data = QPushButton("获取数据")
        set_control_size(self.button_get_data)

        row2 = QHBoxLayout()
        row2.addStretch()
        row2.addWidget(self.ledit_row_mark)
        row2.addWidget(self.ledit_col_mark)
        row2.addWidget(self.button_get_data)
        self.global_layout.addLayout(row2)

    def init_row4(self):
        self.tablewidget = QTableWidget()

        row3 = QHBoxLayout()
        row3.addWidget(self.tablewidget)
        self.global_layout.addLayout(row3)

    def init_row2(self):
        self.ledit_rows_cols = QLineEdit()
        self.ledit_rows_cols.setReadOnly(True)
        set_control_size(self.ledit_rows_cols)

        self.button_transfer_excel = QPushButton("转换为Excel")
        self.button_transfer_excel.setEnabled(False)
        set_control_size(self.button_transfer_excel)

        self.button_open_file = QPushButton("打开文件")
        set_control_size(self.button_open_file)

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("文件总(行号,列号):"))
        row4.addWidget(self.ledit_rows_cols)
        row4.addStretch()
        row4.addWidget(self.button_transfer_excel)
        row4.addWidget(self.button_open_file)
        self.global_layout.addLayout(row4)

    def init_close_row(self):
        self.button_close = QPushButton("关闭程序")
        set_control_size(self.button_close)

        row_close = QHBoxLayout()
        row_close.addStretch()
        row_close.addWidget(self.button_close)
        self.global_layout.addLayout(row_close)
