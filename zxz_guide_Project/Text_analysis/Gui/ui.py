import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Universal_Methods.Universal_Method import Common_Method
from Text_analysis.communication import open_ini, open_json, open_xml, ysopen_excel
from Text_analysis.data_centers import Text_parsing_control as D_C


class Myui(QWidget):
    def __init__(self):
        super(Myui, self).__init__()
        self.D_C = D_C.Data_Center()
        self.logsdata = None
        self.join_ui()
        self.show_ui()

    def join_ui(self):
        self.global_layout = QVBoxLayout()

        self.init_row1()
        self.init_row2()
        self.init_row3()
        self.init_row4()

        self.statusBar = QStatusBar()
        self.global_layout.addWidget(self.statusBar)

    def show_ui(self):
        self.setLayout(self.global_layout)
        self.setFixedSize(QSize(550, 400))
        self.setWindowTitle('读取LOG数据')

    def init_row1(self):
        self.ledit_file_path = QLineEdit()
        self.button_select_file = QPushButton("选择文件")
        self.button_select_file.setFixedSize(QSize(80, 20))
        self.button_select_file.clicked.connect(self.select_file_fun)

        row1 = QHBoxLayout()
        row1.addWidget(self.ledit_file_path)
        row1.addWidget(self.button_select_file)
        self.global_layout.addLayout(row1)

    def init_row3(self):
        self.ledit_row_mark = QLineEdit()
        self.ledit_row_mark.setFixedSize(50, 20)
        self.ledit_row_mark.setPlaceholderText("行号")

        self.ledit_col_mark = QLineEdit()
        self.ledit_col_mark.setFixedSize(50, 20)
        self.ledit_col_mark.setPlaceholderText("列号")

        self.button_get_data = QPushButton("获取数据")
        self.button_get_data.setFixedSize(QSize(80, 20))
        self.button_get_data.clicked.connect(self.get_data_fun)

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
        self.ledit_rows_cols.setFixedSize(QSize(70, 20))
        self.ledit_rows_cols.setReadOnly(True)

        self.button_transfer_excel = QPushButton("转换为Excel")
        self.button_transfer_excel.setFixedSize(QSize(80, 20))
        self.button_transfer_excel.clicked.connect(self.transfer_excel_fun)

        self.button_open_file = QPushButton("打开文件")
        self.button_open_file.setFixedSize(QSize(80, 20))
        self.button_open_file.clicked.connect(self.open_file_fun)

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("文件总(行号,列号):"))
        row4.addWidget(self.ledit_rows_cols)
        row4.addStretch()
        row4.addWidget(self.button_transfer_excel)
        row4.addWidget(self.button_open_file)
        self.global_layout.addLayout(row4)

    def select_file_fun(self):
        file_name, file_type = Common_Method.getOpenFileName()
        self.ledit_file_path.setText(file_name)

    def transfer_excel_fun(self):
        Common_Method.file_transfer_excel(self)
        self.get_signal("转换excel成功 文件在该程序同级目录下")

    def get_data_fun(self):
        row = self.ledit_row_mark.text()
        col = self.ledit_col_mark.text()
        self.D_C.set_row_number(row)
        self.D_C.set_col_number(col)

        self.logsdata.read_data()

    def open_file_fun(self):
        file_path = self.ledit_file_path.text()
        self.D_C.set_file_path(file_path)
        file_type = file_path.split(".")
        file_type = file_type[1]
        print(file_type)
        if file_type == "xlsx":
            self.logsdata = ysopen_excel.File_data()
        elif file_type == "ini":
            self.logsdata = open_ini.File_data(self)
        elif file_type == "json":
            self.logsdata = open_json.File_data(self)
        elif file_type == "xml":
            self.logsdata = open_xml.File_data(self)

        # 实例处理代码对象 并将这个类下的信号 绑定到槽函数上
        self.logsdata._signal.connect(self.get_signal)
        self.logsdata._text.connect(self.get_text)
        self.logsdata._rowcol.connect(self.get_rowcol)

        self.logsdata.initialize_data_to_ui()

    def get_text(self, text):
        data = text.split("@@@")

        if data[0] == "row_and_col":

            self.tablewidget.setRowCount(1)
            self.tablewidget.setColumnCount(1)
            HeaderLabels = ["指定数据"]
            self.tablewidget.setHorizontalHeaderLabels(HeaderLabels)
            item = QTableWidgetItem(str(data[1]))
            self.tablewidget.setItem(0,0,item)

        elif data[0] == "row":
            get_data = data[1].replace("nan", "")
            get_datas = eval(get_data)
            print("格式化后{}".format(get_data))

            self.tablewidget.setRowCount(1)
            self.tablewidget.setColumnCount(len(get_datas))
            for col in range(len(get_datas)):
                item = QTableWidgetItem(str(get_datas[col]))
                self.tablewidget.setItem(0, col, item)

            HeaderLabels = eval(data[2])
            self.tablewidget.setHorizontalHeaderLabels(HeaderLabels)
            self.tablewidget.removeColumn(0)
                
        elif data[0] == "col":
            get_data = data[1].replace("nan", "")
            get_datas = eval(get_data)
            print("格式化后{}".format(get_datas))

            self.tablewidget.setRowCount(len(get_datas))
            self.tablewidget.setColumnCount(1)
            for row in range(len(get_datas)):
                item = QTableWidgetItem(str(get_datas[row]))
                self.tablewidget.setItem(row, 0, item)


            HeaderLabels = [data[2]]
            self.tablewidget.setHorizontalHeaderLabels(HeaderLabels)



        elif data[0] == "all":
            # 转换信号传来的字符串类型文件 转为列表
            get_data = data[1].replace("nan", "")
            get_datas = eval(get_data)

            # 视图控件设置行列数 遍历往里添加数据
            self.tablewidget.setRowCount(len(get_datas))
            self.tablewidget.setColumnCount(len(get_datas[0]))
            for row in range(len(get_datas)):
                for col in range(len(get_datas[row])):
                    item = QTableWidgetItem(str(get_datas[row][col]))
                    self.tablewidget.setItem(row, col, item)

            # 替换视图上的表头，列名
            HeaderLabels = eval(data[2])
            self.tablewidget.setHorizontalHeaderLabels(HeaderLabels)
            self.tablewidget.removeColumn(0)


        else:
            self.statusBar.showMessage("索引超出文件范围")

            

    def get_signal(self, signal):
        self.statusBar.showMessage(signal)
        print("ui槽触发信号{}".format(signal))

    def get_rowcol(self, rowcol):
        self.ledit_rows_cols.setText(rowcol)
        print("ui槽触发行列数{}".format(rowcol))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Myui()
    dialog.show()
    sys.exit(app.exec_())