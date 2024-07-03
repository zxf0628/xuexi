import sys
from PyQt5.QtWidgets import QTableWidgetItem, QApplication

from Universal_Methods.Universal_Method import Common_Method
from Text_analysisV2.Gui.main_ui import Text_analysis_ui
from Text_analysisV2.communication import open_ini, open_json, open_xml, open_excel
from Text_analysisV2.data_centers.data_transfer import Data_Center
from Text_analysisV2.signal_centers.signal_transfer import Signal_Center


class Text_analysis_logic(Text_analysis_ui):
    def __init__(self):
        super(Text_analysis_logic, self).__init__()
        self.show_ui()

        self.data_center = Data_Center()
        self.signal_center = Signal_Center()
        self.logsdata = None

        self.initialize_ui_button_of_signal_connect_to_mySlot_function()
        self.initialize_ui_button_data_update_of_signal_connect_to_mySlot_function()

    # 初始化，ui控件自带的触发信号 绑定到自定义的槽函数上
    def initialize_ui_button_of_signal_connect_to_mySlot_function(self):
        print("Text_analysis_logic->initialize_ui_button_of_signal_connect_to_mySlot_function->")
        self.button_select_file.clicked.connect(self.select_file_fun)
        self.button_get_data.clicked.connect(self.get_data_fun)
        self.button_transfer_excel.clicked.connect(self.transfer_excel_fun)
        self.button_open_file.clicked.connect(self.open_file_fun)
        self.button_close.clicked.connect(self.close)

    # 初始化，ui控件自带的数据更新触发信号 绑定到自定义的槽函数上
    def initialize_ui_button_data_update_of_signal_connect_to_mySlot_function(self):
        print("Text_analysis_logic->initialize_ui_button_data_update_of_signal_connect_to_mySlot_function->")
        self.ledit_row_mark.textChanged.connect(self.ui_data_update_to_data_center)
        self.ledit_col_mark.textChanged.connect(self.ui_data_update_to_data_center)
        self.ledit_file_path.textChanged.connect(self.ui_data_update_to_data_center)

    def ui_data_update_to_data_center(self):
        print("Text_analysis_logic->ui_data_update_to_data_center->")
        row = self.ledit_row_mark.text()
        col = self.ledit_col_mark.text()
        file_path = self.ledit_file_path.text()
        self.data_center.set_row_number(row)
        self.data_center.set_col_number(col)
        if file_path:
            self.data_center.set_file_path(file_path)

    # 初始化，信号中心的信号 绑定到自定义槽函数上
    def initialize_signal_center_of_signal_connect_to_mySlot_function(self):
        print("Text_analysis_logic->initialize_signal_center_of_signal_connect_to_mySlot_function->")
        self.signal_center._signal.connect(self.sin_get_signal)
        self.signal_center._text.connect(self.sin_get_text)
        self.signal_center._row_and_col.connect(self.sin_get_row_and_col)

    # ui控件触发的自定义槽函数
    def select_file_fun(self):
        file_name, file_type = Common_Method.getOpenFileName()
        self.ledit_file_path.setText(file_name)
        print("Text_analysis_logic->select_file_fun->：{}".format(file_name))
        file_types = file_name.split(".")
        if file_types[1] == "log":
            self.button_transfer_excel.setEnabled(True)
        else:
            self.button_transfer_excel.setEnabled(False)

    def transfer_excel_fun(self):
        print("Text_analysis_logic->transfer_excel_fun->")
        try:
            path = self.data_center.get_file_path()
            flag = Common_Method.file_transfer_excel(path)
            if flag:
                self.sin_get_signal("转换excel成功 文件在该程序同级目录下")
                self.select_file_fun()
        except Exception as reason:
            self.sin_get_signal("所选择文件类型异常 只支持log")
            print("异常：Text_analysis_logic->transfer_excel_fun->{}".format(reason))

    def get_data_fun(self):
        print("Text_analysis_logic->get_data_fun->")
        self.logsdata.read_data()

    def open_file_fun(self):
        file_path = self.data_center.get_file_path()
        file_types = file_path.split(".")
        print("Text_analysis_logic->open_file_fun->运行的文件类型：{}".format(file_types[1]))
        if file_types[1] == "xlsx":
            self.logsdata = open_excel.File_data()
        elif file_types[1] == "ini":
            self.logsdata = open_ini.File_data(self)
        elif file_types[1] == "json":
            self.logsdata = open_json.File_data(self)
        elif file_types[1] == "xml":
            self.logsdata = open_xml.File_data(self)

        # 实例处理代码对象 并将信号中心的信号 绑定到主逻辑界面的槽函数上
        self.initialize_signal_center_of_signal_connect_to_mySlot_function()
        self.logsdata.initialize_row_and_col_to_ui()

    # 信号中心预先声明的信号 绑定的槽函数
    def sin_get_text(self, text):
        data = text.split("@@@")
        print("Text_analysis_logic->sin_get_text->要显示数据的方式:{}".format(data[0]))

        if data[0] == "row_and_col":
            self.tablewidget.setRowCount(1)
            self.tablewidget.setColumnCount(1)
            HeaderLabels = ["指定数据"]
            self.tablewidget.setHorizontalHeaderLabels(HeaderLabels)
            item = QTableWidgetItem(str(data[1]))
            self.tablewidget.setItem(0, 0, item)

        elif data[0] == "row":
            get_data = data[1].replace("nan", "")
            get_datas = eval(get_data)

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

            self.tablewidget.setRowCount(len(get_datas))
            self.tablewidget.setColumnCount(1)
            for row in range(len(get_datas)):
                item = QTableWidgetItem(str(get_datas[row]))
                self.tablewidget.setItem(row, 0, item)

            HeaderLabels = [data[2]]
            self.tablewidget.setHorizontalHeaderLabels(HeaderLabels)

        elif data[0] == "all":
            # 删除传来str(全部数据)，去除多余字符，转换为list
            get_data = data[1].replace("nan", "")
            get_datas = eval(get_data)

            # 视图控件设置行列数 遍历往里添加数据
            self.tablewidget.setRowCount(len(get_datas))
            self.tablewidget.setColumnCount(len(get_datas[0]))
            for row in range(len(get_datas)):
                for col in range(len(get_datas[row])):
                    item = QTableWidgetItem(str(get_datas[row][col]))
                    self.tablewidget.setItem(row, col, item)

            # 用列名替换视图上的表头名称
            HeaderLabels = eval(data[2])
            self.tablewidget.setHorizontalHeaderLabels(HeaderLabels)
            self.tablewidget.removeColumn(0)

    def sin_get_signal(self, signal):
        print("Text_analysis_logic->sin_get_signal->：{}".format(signal))
        self.statusBar.showMessage(signal)

    def sin_get_row_and_col(self, row_and_col):
        print("Text_analysis_logic->sin_get_row_and_col->：{}".format(row_and_col))
        if row_and_col == "输入行列号异常":
            self.ledit_rows_cols.clear()
            return
        else:
            self.ledit_rows_cols.setText(row_and_col)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Text_analysis_logic()
    dialog.show()
    sys.exit(app.exec_())