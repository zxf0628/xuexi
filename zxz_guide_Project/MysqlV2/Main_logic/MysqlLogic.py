import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from MysqlV2.communication.operation_myqsl_databases_code import Processing
from MysqlV2.data_centers.data_transfer import Data_Center
from MysqlV2.singal_centers.signal_transfer import Signal_Center
from MysqlV2.Gui.input_ui2 import AddDialog as AddDialog2
from MysqlV2.Gui.main_ui import MainUi

data = {}


class MysqlLogic(MainUi):
    def __init__(self):
        super(MysqlLogic, self).__init__()
        self.set_show_ui()

        self.data_centre = Data_Center()
        self.signal_center = Signal_Center()
        self.column_name = None
        self.operation = None

        self.initialize_ui_control_binding_to_function()
        self.initialize_ui_data_update_to_data_transfer_connect_update_fun()
        self.initialize_Singal_connect_to_groove_fun()

    # ui控件被点击、右键 触发的信号 绑定到主逻辑下函数
    def initialize_ui_control_binding_to_function(self):
        print("MysqlLogic->initialize_ui_control_binding_to_function->")
        self.tableWidget.customContextMenuRequested[QtCore.QPoint].connect(self.context_menu)
        self.button_open_databases.clicked.connect(self.living_example_operation)
        self.button_save_data.clicked.connect(self.fun_save_data)
        self.button_insert_data.clicked.connect(self.fun_open_AddDialog2)
        self.button_to_load_data.clicked.connect(self.fun_load_all_data_to_ui)
        self.button_close.clicked.connect(self.close)

    # ui上数据有改动时，根据这些控件自带的信号 把这些信号与将数据同步到数据中心函数绑定
    def initialize_ui_data_update_to_data_transfer_connect_update_fun(self):
        print("MysqlLogic->initialize_ui_data_update_to_data_transfer_connect_update_fun->")
        # ui界面下拉框控件 选择内容时 将数据写入数据中心
        self.comboBox_select_datatable.activated.connect(self.ui_data_update_to_data_centre)
        self.comboBox_select_databases.activated.connect(self.ui_data_update_to_data_centre)
        self.ComboBox_select_condition_name.activated.connect(self.ui_data_update_to_data_centre)
        self.ComboBox_delete_where_name.activated.connect(self.ui_data_update_to_data_centre)
        self.ComboBox_select_condition_operator.activated.connect(self.ui_data_update_to_data_centre)
        self.ComboBox_delete_where_operator.activated.connect(self.ui_data_update_to_data_centre)

        # ui界面条件文本输入框控件 写入内容时 将数据写入数据中心
        self.LineEdit_select_condition.textChanged.connect(self.ui_data_update_to_data_centre)
        self.LineEdit_delete_where.textChanged.connect(self.ui_data_update_to_data_centre)

    # ui控件被点击（触发了自身信号） 与处理代码类下的方法进行绑定
    def initialize_ui_button_connect_to_operation(self):
        print("MysqlLogic->initialize_ui_button_connect_to_operation->")
        # ui控件点击与处理代码类下的函数绑定槽函数
        self.button_select_condition.clicked.connect(self.operation.ui_button_select_sql)
        self.button_delete_data.clicked.connect(self.operation.ui_button_delete_sql)
        self.button_show_databases_name.clicked.connect(self.operation.ui_button_show_databases_name)
        self.button_select_databases.clicked.connect(self.operation.ui_button_select_databases_name)
        self.button_select_datatable.clicked.connect(self.operation.ui_button_select_datalabel_name)

    # 信号中心信号绑定到 主逻辑下函数
    def initialize_Singal_connect_to_groove_fun(self):
        print("MysqlLogic->initialize_Singal_connect_to_groove_fun->")
        # 处理代码自定义信号与 绑定ui界面函数
        self.signal_center._databases_name.connect(self.sin_get_databases_name)
        self.signal_center._datalabel_name.connect(self.sin_get_datalabel_name)
        self.signal_center._datalabel_column_name.connect(self.sin_get_datalabel_column_name)
        self.signal_center._present_data.connect(self.sin_get_processing_data)
        self.signal_center._statusBar.connect(self.sin_get_hint_singal_to_statusBar)

    # 将ui上现数据 全部同步到数据中心
    def ui_data_update_to_data_centre(self):
        print("MysqlLogic->ui_data_update_to_data_centre->")

        comboBox_select_databases = self.comboBox_select_databases.currentText()
        comboBox_select_datatable = self.comboBox_select_datatable.currentText()

        LineEdit_select_condition_value = self.LineEdit_select_condition.text()
        LineEdit_delete_where_value = self.LineEdit_delete_where.text()
        ComboBox_select_condition_key = self.ComboBox_select_condition_name.currentText()
        ComboBox_delete_condition_key = self.ComboBox_delete_where_name.currentText()
        ComboBox_select_condition_operator = self.ComboBox_select_condition_operator.currentText()
        ComboBox_delete_condition_operator = self.ComboBox_delete_where_operator.currentText()

        if comboBox_select_databases:
            self.data_centre.set_databases_name(comboBox_select_databases)
        if comboBox_select_datatable:
            self.data_centre.set_datalabel_name(comboBox_select_datatable)
        if LineEdit_select_condition_value:
            self.data_centre.set_select_condition_vlaue(LineEdit_select_condition_value)
        if LineEdit_delete_where_value:
            self.data_centre.set_sdelete_condition_vlaue(LineEdit_delete_where_value)
        if ComboBox_select_condition_key:
            self.data_centre.set_select_condition_key(ComboBox_select_condition_key)
        if ComboBox_delete_condition_key:
            self.data_centre.set_delete_condition_key(ComboBox_delete_condition_key)
        if ComboBox_select_condition_operator:
            self.data_centre.set_select_condition_operator(ComboBox_select_condition_operator)
        if ComboBox_delete_condition_operator:
            self.data_centre.set_delete_condition_operator(ComboBox_delete_condition_operator)

    # 信号中心根据预设的信号名称，实现的相应槽函数功能
    def sin_get_databases_name(self, databases_name):
        databases_names = databases_name.split(",")
        self.comboBox_select_databases.addItems(databases_names)
        print("MysqlLogic->sin_get_databases_name->{}".format(databases_names))

    def sin_get_datalabel_name(self, datalabel_name):
        datalabel_names = datalabel_name.split(",")
        self.comboBox_select_datatable.addItems(datalabel_names)
        print("MysqlLogic->sin_get_datalabel_name->{}".format(datalabel_names))

    def sin_get_datalabel_column_name(self, datalabel_column_name):
        print("MysqlLogic->sin_get_datalabel_column_name->{}".format(datalabel_column_name))
        self.LineEdit_label_column_name.clear()
        self.ComboBox_select_condition_name.clear()
        self.ComboBox_delete_where_name.clear()
        self.ComboBox_select_condition_operator.clear()
        self.ComboBox_delete_where_operator.clear()

        self.LineEdit_label_column_name.setText(datalabel_column_name)
        self.column_name = datalabel_column_name.split(",")

        # 将处理代码返回的字符串类型的 列名数据，写入到数据中心（）
        self.data_centre.set_label_column_name(self.column_name)
        print("MysqlLogic->sin_get_datalabel_column_name->写入数据中心的列名类型:{}".format(type(self.column_name)))

        operator = ["=", "!=", ">", "<", ">=", "<="]
        self.ComboBox_select_condition_name.addItems(self.column_name)
        self.ComboBox_delete_where_name.addItems(self.column_name)
        self.ComboBox_select_condition_operator.addItems(operator)
        self.ComboBox_delete_where_operator.addItems(operator)

        # 设置下拉框中默认选项
        self.ComboBox_select_condition_operator.setCurrentIndex(0)
        self.ComboBox_delete_where_name.setCurrentIndex(0)
        self.ComboBox_select_condition_name.setCurrentIndex(0)
        self.ComboBox_delete_where_operator.setCurrentIndex(0)

        self.ui_data_update_to_data_centre()

    def sin_get_processing_data(self, processing_data):
        print("MysqlLogic->sin_get_processing_data->{}".format(processing_data))
        datas = eval(processing_data)
        print("MysqlLogic->sin_get_processing_data->将传来的字符类型数据转为二维数组{}".format(datas))
        self.tableWidget.setRowCount(len(datas))
        self.tableWidget.setColumnCount(len(datas[0]))
        for i in range(len(datas)):
            for j in range(len(datas[i])):
                item = QTableWidgetItem(str(datas[i][j]))
                self.tableWidget.setItem(i, j, item)

        # 根据数据表数据列名，设置ui界面上表头
        HeaderLabels = self.data_centre.get_label_column_name()
        self.tableWidget.setHorizontalHeaderLabels(HeaderLabels)

    def sin_get_hint_singal_to_statusBar(self, singal):
        print("MysqlLogic->sin_get_hint_singal_to_statusBar->{}".format(singal))
        self.statusBar.showMessage(singal)

    # 打开数据表时，实例一个处理代码类 类内有相应的处理数据方法
    def living_example_operation(self):
        print("MysqlLogic->living_example_operation->")
        self.operation = Processing()
        self.initialize_ui_button_connect_to_operation()

        if self.operation is not None:
            self.sin_get_hint_singal_to_statusBar("打开数据库")

    # 运行显示添加数据界面窗口，实例一个InputDialog2类
    def fun_open_AddDialog2(self):
        print("MysqlLogic->fun_open_AddDialog2->")
        di = InputDialog2()
        ok = di.exec_()
        if not ok:
            return

        # 拿到输入窗口下全部的 单行文本输入对象 下的内容 顺序与创建顺序一致,并存入全局变量字典中
        row_data = di.Input_field_object_texts()
        data[row_data[0]] = row_data[1:]
        print("MysqlLogic->fun_open_AddDialog2->弹框窗口内容添加进data字典后内容：{}".format(data))
        
        # 向UI数据表视图上 添加显示数据，将保存按钮置为高亮
        self.insert_row_data_to_ui(row_data)
        self.button_save_data.setEnabled(True)

    # 向数据表视图内最后一行插入一条数据，并在全局变量内也添加内容
    def insert_row_data_to_ui(self, row_data):
        print("MysqlLogic->fun_open_AddDialog2->：{}".format(row_data))
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        col = 0
        for i in row_data:
            cell = QTableWidgetItem(str(i))
            self.tableWidget.setItem(row, col, cell)
            col += 1

    # 数据表内全部数据加载到视图上
    def fun_load_all_data_to_ui(self):
        print("MysqlLogic->fun_load_all_data_to_ui->")
        if self.button_save_data.isEnabled():
            r = QMessageBox.warning(self, "警告", "是否覆盖当前表格数据", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.No:
                return
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()

        # 将数据存入全局变量data下，达到同步数据
        results = self.operation.load_all_data()
        for (sid, name, sex, age, grade) in results:
            data[sid] = [name, sex, age, grade]
        print("MysqlLogic->fun_load_all_data_to_ui->将数据表全部数据存入到变量中后：{}".format(data))

        # 将ui界面上保存按钮置为高亮
        self.button_save_data.setEnabled(True)

    # 根据类内运行的data字典，重新保存数据
    def fun_save_data(self):
        print("MysqlLogic->fun_save_data->")
        z = self.operation.save_data(data)
        if z:
            self.button_save_data.setEnabled(False)
            self.sin_get_hint_singal_to_statusBar("保存数据成功")
        else:
            QMessageBox.critical(self, "错误", "数据格式有误，请检查")

    # 右键菜单 弹出选项菜单 修改与删除
    def context_menu(self, pos):
        print("MysqlLogic->context_menu->：{}".format(pos))
        pop_menu = QMenu()
        change_new_event = pop_menu.addAction("修改行")
        delete_event = pop_menu.addAction("删除行")
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))

        if action == change_new_event:
            print("MysqlLogic->context_menu->修改行功能")
            item = self.tableWidget.selectedItems()
            row = item[0].row()
            id = self.tableWidget.item(row, 0).text()
            di = InputDialog2(sid=id)
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
            print("MysqlLogic->context_menu->删除行功能")
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.No:
                return
            items = self.tableWidget.selectedItems()
            print("MysqlLogic->context_menu->删除行功能，拿到UI界面上行号的表格对象：{}".format(items))

            # 拿到UI上的删除行数的表格对象，将行号放入一个列表，该行第一个数据就是id,删除存储数据data变量中一个键，
            # 在删除视图上的行数数据，就是删除变量数据，删除视图上的 达到数据的实时同步
            if items:
                selected_rows = []
                for i in items:
                    row = i.row()
                    if row not in selected_rows:
                        selected_rows.append(row)
                    print("MysqlLogic->context_menu->删除行功能，selected_rows内容：{}".format(selected_rows))
                selected_rows = sorted(selected_rows, reverse=True)
                for r in selected_rows:
                    # 拿到id 好用于删除
                    sid = self.tableWidget.item(r, 0).text()
                    del data[sid]
                    self.tableWidget.removeRow(r)
            self.button_save_data.setEnabled(True)


class InputDialog2(AddDialog2):
    def __init__(self, sid=None):
        super(InputDialog2, self).__init__()
        self.setupUI()
        self.sid = sid
        self.buttonsBox.accepted.connect(self.check)

        if sid:
            print("InputDialog2->__init__->传入sid为修改功能弹框sid：{}".format(sid))
            # 传入sid时 通过这个sid在data全局变量中拿数据，存入表格视图内
            lineEdit_objects = self.get_ui_all_control_object(QLineEdit)
            lineEdit_objects[0].setText(sid)
            data_location = 1
            for i in range(len(lineEdit_objects[1:])):
                lineEdit_objects[data_location].setText(data[sid][i])

    def check(self):
        print("InputDialog2->check->")
        lineEdit_objects = self.get_ui_all_control_object(QLineEdit)
        sid = lineEdit_objects[0].text()
        name = lineEdit_objects[1].text()
        print("InputDialog2->check->拿到弹框中数据 id/name：{}{}".format(sid,name))
        if sid in data and self.sid not in data:
            QMessageBox.warning(self, "警告", "该学号已存在!", QMessageBox.Ok)
            return
        if not sid:
            QMessageBox.warning(self, "警告", "学号为必填项!", QMessageBox.Ok)
            return
        if not name:
            QMessageBox.warning(self, "警告", "姓名为必填项!", QMessageBox.Ok)
            return

        self.accept()

    def Input_field_object_texts(self):

        print("InputDialog2->Input_field_object_texts->")
        textlist = []
        lineEdit_objects = self.get_ui_all_control_object(QLineEdit)
        for i in lineEdit_objects:
            textlist.append(i.text())
        return textlist

    def get_ui_all_control_object(self,control_name=QLineEdit):
        print("InputDialog2->get_ui_all_control_object->:{}".format(control_name))
        control_object = self.findChildren(control_name)
        return control_object


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     zxf = MysqlLogic()
#     zxf.show()
#     sys.exit(app.exec_())