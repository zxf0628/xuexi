import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Mysql.communication.operation_myqsl_databases_code import Processing
from Mysql.data_centers.data_transfer import Data_Center


class Myui(QWidget):
    def __init__(self):
        super(Myui, self).__init__()
        self.data_centre = Data_Center()
        self.join_ui()
        self.show_ui()

    def join_ui(self):
        self.right_ui()
        self.global_layout = QHBoxLayout()

        self.present_data = QTextEdit()
        self.set_ui_control_size(self.present_data, 280, 370)
        self.global_layout.addWidget(self.present_data)
        self.global_layout.addLayout(self.right_layout)

    def show_ui(self):
        self.my_ui = QWidget()
        self.my_ui.setLayout(self.global_layout)
        self.my_ui.setFixedSize(QSize(600, 400))
        self.my_ui.setWindowTitle('查询数据库')
        # self.my_ui.show()

    def right_ui(self):
        self.right_layout = QVBoxLayout()
        self.init_row1()
        self.init_row2()
        self.init_row3()
        self.init_row4()
        self.init_row5()
        self.init_row6()
        self.init_row7()
        self.init_row8()
        self.init_row9()

    def set_ui_control_size(self, control, length=80, wide=30):
        control.setFixedSize(QSize(int(length), int(wide)))

    def init_row1(self):
        self.button_open_databases = QPushButton("打开mysql数据库")
        self.button_open_databases.clicked.connect(self.living_example_operation)
        self.button_open_sqlite_databases = QPushButton("打开sqlite数据库")
        self.button_open_sqlite_databases.clicked.connect(self.living_example_sqlite_operation)
        self.button_show_databases_name = QPushButton("显示库名")
        self.right_layout.addWidget(self.button_open_databases)
        # self.right_layout.addWidget(self.button_open_sqlite_databases)
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
        self.Label_label_column_name = QLabel("列名展示：")

        row4 = QHBoxLayout()
        row4.addWidget(self.Label_label_column_name)
        row4.addWidget(self.LineEdit_label_column_name)

        self.right_layout.addLayout(row4)

    def init_row5(self):
        self.LineEdit_select_condition = QLineEdit()
        self.LineEdit_select_condition.setPlaceholderText("条件")
        self.button_select_condition = QPushButton("查询数据")

        row5 = QHBoxLayout()
        row5.addWidget(self.LineEdit_select_condition)
        row5.addWidget(self.button_select_condition)

        self.right_layout.addLayout(row5)

    def init_row6(self):
        self.LineEdit_update_key = QLineEdit()
        self.LineEdit_update_key.setPlaceholderText("列名 ，分割")
        self.LineEdit_update_value = QLineEdit()
        self.LineEdit_update_value.setPlaceholderText("值 ，分割")
        self.LineEdit_update_where = QLineEdit()
        self.LineEdit_update_where.setPlaceholderText("条件")

        self.button_update_data = QPushButton("修改数据")

        row6 = QHBoxLayout()
        row6.addWidget(self.LineEdit_update_key)
        row6.addWidget(QLabel(":"))
        row6.addWidget(self.LineEdit_update_value)
        row6.addWidget(self.LineEdit_update_where)
        row6.addWidget(self.button_update_data)

        self.right_layout.addLayout(row6)

    def init_row7(self):
        self.LineEdit_delete_where = QLineEdit()
        self.LineEdit_delete_where.setPlaceholderText("条件")
        self.button_delete_data = QPushButton("删除数据")

        row7 = QHBoxLayout()
        row7.addWidget(self.LineEdit_delete_where)
        row7.addWidget(self.button_delete_data)

        self.right_layout.addLayout(row7)

    def init_row8(self):
        self.LineEdit_insert_data = QLineEdit()
        self.LineEdit_insert_data.setPlaceholderText("数据 ，分割")
        self.button_insert_data = QPushButton("增加数据")

        row8 = QHBoxLayout()
        row8.addWidget(self.LineEdit_insert_data)
        row8.addWidget(self.button_insert_data)

        self.right_layout.addLayout(row8)

    def init_row9(self):
        self.statusBar = QStatusBar()
        self.set_ui_control_size(self.statusBar, 200, 40)
        self.right_layout.addWidget(self.statusBar)

    def button_connet_operation(self):
        # ui控件与处理代码绑定函数
        self.button_select_condition.clicked.connect(self.operation.select_sql)
        self.button_update_data.clicked.connect(self.operation.update_sql)
        self.button_delete_data.clicked.connect(self.operation.delete_sql)
        self.button_insert_data.clicked.connect(self.operation.insert_sql)

        self.button_show_databases_name.clicked.connect(self.operation.ui_button_show_databases_name)
        self.button_select_databases.clicked.connect(self.operation.ui_butthon_select_databases_name)
        self.comboBox_select_databases.activated.connect(self.set_databases_name_to_dc)
        self.button_select_datatable.clicked.connect(self.operation.ui_button_select_datalabel_name)
        self.comboBox_select_datatable.activated.connect(self.set_datalabel_name_to_dc)

        # 处理代码自定义信号与 绑定ui界面函数
        self.operation._databases_name.connect(self.sin_get_databases_name)
        self.operation._datalabel_name.connect(self.sin_get_datalabel_name)
        self.operation._datalabel_column_name.connect(self.sin_get_datalabel_column_name)
        self.operation._present_data.connect(self.sin_get_processing_data)
        self.operation._statusBar.connect(self.sin_get_hint_singal_to_statusBar)

        self.LineEdit_select_condition.textChanged.connect(self.ui_data_set_to_data_centre)
        self.LineEdit_update_key.textChanged.connect(self.ui_data_set_to_data_centre)

        self.LineEdit_update_value.textChanged.connect(self.ui_data_set_to_data_centre)
        self.LineEdit_update_where.textChanged.connect(self.ui_data_set_to_data_centre)
        self.LineEdit_delete_where.textChanged.connect(self.ui_data_set_to_data_centre)
        self.LineEdit_insert_data.textChanged.connect(self.ui_data_set_to_data_centre)

    def living_example_operation(self):
        self.operation = Processing()
        self.button_connet_operation()

        self.sin_get_hint_singal_to_statusBar("打开数据库")

    def living_example_sqlite_operation(self):
        self.operation = sqlite_Processing()
        self.button_connet_operation()

        self.sin_get_hint_singal_to_statusBar("打开数据库")

    def sin_get_databases_name(self, databases_name):
        databases_name = list(databases_name.split(","))
        self.comboBox_select_databases.addItems(databases_name)

    def sin_get_datalabel_name(self, datalabel_name):
        datalabel_name = list(datalabel_name.split(","))
        self.comboBox_select_datatable.addItems(datalabel_name)

    def sin_get_datalabel_column_name(self, datalabel_column_name):
        self.LineEdit_label_column_name.setText(datalabel_column_name)

    def sin_get_processing_data(self, processing_data):
        self.present_data.clear()
        self.present_data.setPlainText(processing_data)

    def sin_get_hint_singal_to_statusBar(self, singal):
        self.statusBar.showMessage(singal)

    def set_databases_name_to_dc(self):
        databases_name = self.comboBox_select_databases.currentText()
        self.data_centre.set_databases_name(databases_name)

    def set_datalabel_name_to_dc(self):
        datalabel_name = self.comboBox_select_datatable.currentText()
        self.data_centre.set_datalabel_name(datalabel_name)

    def ui_data_set_to_data_centre(self):
        LineEdit_select_condition_content = self.LineEdit_select_condition.text()
        LineEdit_update_key_content = self.LineEdit_update_key.text()
        LineEdit_update_value_content = self.LineEdit_update_value.text()
        LineEdit_update_where_content = self.LineEdit_update_where.text()
        LineEdit_delete_where_content = self.LineEdit_delete_where.text()
        LineEdit_insert_data_content = self.LineEdit_insert_data.text()

        if LineEdit_select_condition_content: self.data_centre.set_select_conditions(LineEdit_select_condition_content)
        if LineEdit_update_key_content: self.data_centre.set_update_keys(LineEdit_update_key_content)
        if LineEdit_update_value_content: self.data_centre.set_update_vlaues(LineEdit_update_value_content)
        if LineEdit_update_where_content: self.data_centre.set_update_conditions(LineEdit_update_where_content)
        if LineEdit_delete_where_content: self.data_centre.set_delete_conditions(LineEdit_delete_where_content)
        if LineEdit_insert_data_content: self.data_centre.set_insert_vlaues(LineEdit_insert_data_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    zxf = Myui()
    zxf.my_ui.show()
    sys.exit(app.exec_())
