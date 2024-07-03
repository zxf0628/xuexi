import sys

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Mysql.communication.operation_myqsl_databases_code import Processing
from Mysql.data_centers.data_transfer import Data_Center
from Mysql.Gui.input_ui import AddDialog as AddDialog1
from Mysql.Gui.input_ui2 import AddDialog as AddDialog2

data = {}


class Myui(QWidget):
    def __init__(self):
        super(Myui, self).__init__()
        self.data_centre = Data_Center()
        self.join_ui()
        self.show_ui()

    # ui界面拼接
    def join_ui(self):
        self.right_ui()
        self.global_layout = QHBoxLayout()

        self.tableWidget = QTableWidget()
        self.global_layout.addWidget(self.tableWidget)
        self.global_layout.addLayout(self.right_layout)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested[QtCore.QPoint].connect(self.context_menu)

    def show_ui(self):
        # self.join_ui()
        self.setLayout(self.global_layout)
        self.setFixedSize(QSize(600, 400))
        self.setWindowTitle('查询数据库')
        # self.my_ui.show()

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
        self.button_open_databases.clicked.connect(self.living_example_operation)

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
        self.button_save_data.clicked.connect(self.fun_save_data)
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
        self.button_insert_data.clicked.connect(self.fun_open_AddDialog2)

        row8 = QHBoxLayout()
        row8.addWidget(self.button_insert_data)

        self.right_layout.addLayout(row8)

    def init_row9_statusBar(self):
        self.statusBar = QStatusBar()
        self.set_ui_control_size(self.statusBar, 200, 40)
        self.right_layout.addWidget(self.statusBar)

    def init_row10_close(self):
        self.button_close = QPushButton("关闭数据连接")
        self.button_close.clicked.connect(self.close)

        self.right_layout.addWidget(self.button_close)

    def init_row11_to_load_data(self):
        self.button_to_load_data = QPushButton("加载数据")

        self.right_layout.addWidget(self.button_to_load_data)


    # 槽函数
    def sin_get_databases_name(self, databases_name):
        databases_name = list(databases_name.split(","))
        self.comboBox_select_databases.addItems(databases_name)

    def sin_get_datalabel_name(self, datalabel_name):
        datalabel_name = list(datalabel_name.split(","))
        self.comboBox_select_datatable.addItems(datalabel_name)

    def sin_get_datalabel_column_name(self, datalabel_column_name):
        self.LineEdit_label_column_name.clear()
        self.ComboBox_select_condition_name.clear()
        self.ComboBox_delete_where_name.clear()
        self.ComboBox_select_condition_operator.clear()
        self.ComboBox_delete_where_operator.clear()

        self.LineEdit_label_column_name.setText(datalabel_column_name)
        self.column_name = list(datalabel_column_name.split(","))
        self.data_centre.set_label_column_name(self.column_name)
        operator = ["=", "!=", ">", "<", ">=", "<="]
        self.ComboBox_select_condition_name.addItems(self.column_name)
        self.ComboBox_select_condition_name.setCurrentIndex(0)
        self.ComboBox_delete_where_name.addItems(self.column_name)
        self.ComboBox_delete_where_name.setCurrentIndex(0)
        self.ComboBox_select_condition_operator.addItems(operator)
        self.ComboBox_select_condition_operator.setCurrentIndex(0)
        self.ComboBox_delete_where_operator.addItems(operator)
        self.ComboBox_delete_where_operator.setCurrentIndex(0)
        self.ui_data_set_to_data_centre()

    def sin_get_processing_data(self, processing_data):
        data = eval(processing_data)
        print("ui界面收到的查询数据处理为元组：{}".format(data))
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for i in range(len(data)):
            for j in range(len(data[i])):
                item = QTableWidgetItem(str(data[i][j]))
                self.tableWidget.setItem(i, j, item)

        HeaderLabels = self.data_centre.get_label_column_name()
        HeaderLabels = HeaderLabels.split(",")
        self.tableWidget.setHorizontalHeaderLabels(HeaderLabels)

    def sin_get_hint_singal_to_statusBar(self, singal):
        self.statusBar.showMessage(singal)

    # 界面触发函数
    def living_example_operation(self):
        self.operation = Processing()
        self.button_connet_operation()

        self.sin_get_hint_singal_to_statusBar("打开数据库")

    def button_connet_operation(self):
        # ui控件与处理代码绑定函数
        self.button_select_condition.clicked.connect(self.operation.select_sql)
        self.button_delete_data.clicked.connect(self.operation.delete_sql)
        self.button_save_data.clicked.connect(self.fun_save_data)
        self.button_to_load_data.clicked.connect(self.fun_to_load_all_data)
        self.button_show_databases_name.clicked.connect(self.operation.ui_button_show_databases_name)
        self.button_select_databases.clicked.connect(self.operation.ui_butthon_select_databases_name)
        self.button_select_datatable.clicked.connect(self.operation.ui_button_select_datalabel_name)

        # ui界面下拉框控件 选择内容时 将数据写入数据中心
        self.comboBox_select_datatable.activated.connect(self.set_datalabel_name_to_dc)
        self.comboBox_select_databases.activated.connect(self.set_databases_name_to_dc)
        self.ComboBox_select_condition_name.activated.connect(self.ui_data_set_to_data_centre)
        self.ComboBox_delete_where_name.activated.connect(self.ui_data_set_to_data_centre)
        self.ComboBox_select_condition_operator.activated.connect(self.ui_data_set_to_data_centre)
        self.ComboBox_delete_where_operator.activated.connect(self.ui_data_set_to_data_centre)

        # ui界面条件文本输入框控件 选择内容时 将数据写入数据中心
        self.LineEdit_select_condition.textChanged.connect(self.ui_data_set_to_data_centre)
        self.LineEdit_delete_where.textChanged.connect(self.ui_data_set_to_data_centre)

        # 处理代码自定义信号与 绑定ui界面函数
        self.operation._databases_name.connect(self.sin_get_databases_name)
        self.operation._datalabel_name.connect(self.sin_get_datalabel_name)
        self.operation._datalabel_column_name.connect(self.sin_get_datalabel_column_name)
        self.operation._present_data.connect(self.sin_get_processing_data)
        self.operation._statusBar.connect(self.sin_get_hint_singal_to_statusBar)

    def ui_data_set_to_data_centre(self):
        LineEdit_select_condition_value = self.LineEdit_select_condition.text()
        LineEdit_delete_where_value = self.LineEdit_delete_where.text()
        ComboBox_select_condition_key = self.ComboBox_select_condition_name.currentText()
        ComboBox_delete_condition_key = self.ComboBox_delete_where_name.currentText()
        ComboBox_select_condition_operator = self.ComboBox_select_condition_operator.currentText()
        ComboBox_delete_condition_operator = self.ComboBox_delete_where_operator.currentText()

        if LineEdit_select_condition_value: self.data_centre.set_select_condition_vlaue(LineEdit_select_condition_value)
        if LineEdit_delete_where_value: self.data_centre.set_sdelete_condition_vlaue(LineEdit_delete_where_value)

        if ComboBox_select_condition_key: self.data_centre.set_select_condition_key(ComboBox_select_condition_key)
        if ComboBox_delete_condition_key: self.data_centre.set_delete_condition_key(ComboBox_delete_condition_key)
        if ComboBox_select_condition_operator: self.data_centre.set_select_condition_operator(
            ComboBox_select_condition_operator)
        if ComboBox_delete_condition_operator: self.data_centre.set_delete_condition_operator(
            ComboBox_delete_condition_operator)

    def set_databases_name_to_dc(self):
        databases_name = self.comboBox_select_databases.currentText()
        self.data_centre.set_databases_name(databases_name)

    def set_datalabel_name_to_dc(self):
        datalabel_name = self.comboBox_select_datatable.currentText()
        self.data_centre.set_datalabel_name(datalabel_name)

    # 添加数据界面运行
    def fun_open_AddDialog1(self):
        di = InputDialog1()
        ok = di.exec_()
        if not ok:
            return
        sid = di.student_id_Field.text()
        name = di.name_Field.text()
        sex = di.sex_Field.text()
        age = di.age_Field.text()
        grade = di.grade_Field.text()
        data[sid] = [name, sex, age, grade]
        self.inser_row(self.tableWidget.rowCount(),sid, name, sex, age,grade)
        self.button_save_data.setEnabled(True)

    def fun_open_AddDialog2(self):
        di = InputDialog2()
        ok = di.exec_()
        if not ok:
            return

        row_data = di.Input_field_object()
        data[row_data[0]] = row_data[1:]
        print("添加方法二添加后data字典：{}".format(data))

        self.inser_row2(self.tableWidget, row_data)
        self.button_save_data.setEnabled(True)

    # 向视图内插入一条数据
    def inser_row(self, row, sid, name, sex, age, grade):
        sid_item = QTableWidgetItem(sid)
        name_item = QTableWidgetItem(name)
        sex_item = QTableWidgetItem(sex)
        age_item = QTableWidgetItem(age)
        grade_item = QTableWidgetItem(grade)
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, sid_item)
        self.tableWidget.setItem(row, 1, name_item)
        self.tableWidget.setItem(row, 2, sex_item)
        self.tableWidget.setItem(row, 3, age_item)
        self.tableWidget.setItem(row, 4, grade_item)

    def inser_row2(self, tablewidget, row_data):
        row = tablewidget.rowCount()
        tablewidget.setRowCount(row + 1)
        col = 0
        for i in row_data:
            cell = QTableWidgetItem(str(i))
            tablewidget.setItem(row, col, cell)
            col += 1

    # 数据表全部数据加载到视图上
    def fun_to_load_all_data(self):
        if self.button_save_data.isEnabled():
            r = QMessageBox.warning(self, "警告", "是否覆盖当前表格数据", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.No:
                return
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()

        results = self.operation.ui_butthon_to_load_all_data()

        # 将数据存入该类的data变量下，为后续调用数据准备
        for (sid, name, sex, age, grade) in results:
            data[sid] = [name, sex, age, grade]
        print("data全部数据：{}".format(data))

        self.button_save_data.setEnabled(True)

    # 根据类内运行的data字典，重新保存数据
    def fun_save_data(self):
        z = self.operation.ui_butthon_save_data(data)
        if z:
            self.button_save_data.setEnabled(False)
            self.sin_get_hint_singal_to_statusBar("保存数据成功")
        else:
            QMessageBox.critical(self, "错误", "数据格式有误，请检查")

    # 右键菜单 选择修改与删除
    def context_menu(self, pos):
        pop_menu = QMenu()
        change_new_event = pop_menu.addAction("修改行")
        delete_event = pop_menu.addAction("删除行")
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))

        if action == change_new_event:
            item = self.tableWidget.selectedItems()
            row = item[0].row()
            id = self.tableWidget.item(row, 0).text()
            di = InputDialog1(sid=id)
            ok = di.exec_()
            if not ok:
                return
            sid = di.student_id_Field.text()
            name = di.name_Field.text()
            sex = di.sex_Field.text()
            age = di.age_Field.text()
            grade = di.grade_Field.text()
            print("before:", id)
            print("after:", sid)
            self.tableWidget.item(row, 0).setText(sid)
            self.tableWidget.item(row, 1).setText(name)
            self.tableWidget.item(row, 2).setText(sex)
            self.tableWidget.item(row, 3).setText(age)
            self.tableWidget.item(row, 4).setText(grade)
            data[sid] = [name, sex, age, grade]
            if id != sid:
                del data[id]
            self.button_save_data.setEnabled(True)
        elif action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.No:
                return
            items = self.tableWidget.selectedItems()
            if items:
                selected_rows = []
                for i in items:
                    row = i.row()
                    if row not in selected_rows:
                        selected_rows.append(row)
                selected_rows = sorted(selected_rows, reverse=True)
                for r in selected_rows:
                    sid = self.tableWidget.item(r, 0).text()
                    del data[sid]
                    self.tableWidget.removeRow(r)
            self.button_save_data.setEnabled(True)



class InputDialog1(AddDialog1):
    def __init__(self, sid=None):
        super(InputDialog1, self).__init__()
        self.setupUI()
        self.sid = sid
        self.buttonsBox.accepted.connect(self.check)

        if sid:
            self.student_id_Field.setText(sid)
            self.name_Field.setText(data[sid][0])
            self.sex_Field.setText(data[sid][1])
            self.age_Field.setText(data[sid][2])
            self.grade_Field.setText(data[sid][3])

    def check(self):
        sid = self.student_id_Field.text()
        name = self.name_Field.text()
        print("ui处理界面拿到弹框中数据：{}".format(sid))
        if sid in data and self.sid not in data:
            r = QMessageBox.warning(self, "警告", "该学号已存在!", QMessageBox.Ok)
            return
        if not sid:
            r = QMessageBox.warning(self, "警告", "学号为必填项!", QMessageBox.Ok)
            return
        if not name:
            r = QMessageBox.warning(self, "警告", "姓名为必填项!", QMessageBox.Ok)
            return

        self.accept()


class InputDialog2(AddDialog2):
    def __init__(self, sid=None):
        super(InputDialog2, self).__init__()
        self.setupUI()
        self.sid = sid
        self.buttonsBox.accepted.connect(self.check)

        if sid:
            lineEdit_objects = self.findChildren(QLineEdit)
            lineEdit_objects[0].setText(sid)
            data_location = 1
            for i in range(len(lineEdit_objects[1:])):
                lineEdit_objects[data_location].setText(data[sid][i])

    def check(self):
        lineEdit_objects = self.findChildren(QLineEdit)
        sid = lineEdit_objects[0].text()
        name = lineEdit_objects[1].text()
        print("ui处理界面拿到弹框中数据：{}".format(sid))
        if sid in data and self.sid not in data:
            r = QMessageBox.warning(self, "警告", "该学号已存在!", QMessageBox.Ok)
            return
        if not sid:
            r = QMessageBox.warning(self, "警告", "学号为必填项!", QMessageBox.Ok)
            return
        if not name:
            r = QMessageBox.warning(self, "警告", "姓名为必填项!", QMessageBox.Ok)
            return

        self.accept()

    def Input_field_object(self):
        textlist = []
        lineEdit_objects = self.findChildren(QLineEdit)
        for i in lineEdit_objects:
            textlist.append(i.text())
        return textlist


if __name__ == "__main__":
    app = QApplication(sys.argv)
    zxf = Myui()
    zxf.show()
    sys.exit(app.exec_())
