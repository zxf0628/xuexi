from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, \
    QTableWidgetItem, QDialog, QMenu, QAction, QHeaderView
from PyQt5.QtCore import pyqtSlot, QMetaObject
import sys
from ui import Ui_MainWindow
from input_dialog import Ui_Dialog_input
from info import Ui_Dialog_info
import pymysql

data = {}


class Demo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)
        self.setupUi(self)
        self.init()
        # self.tableWidget.setRowCount(1)
        # QMetaObject.connectSlotsByName(self)

    def init(self):
        self.button_save.setEnabled(False)
        # self.button_search.clicked.connect(self.func)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested[QtCore.QPoint].connect(self.context_menu)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.line_id.setPlaceholderText("请输入一个学号")

    # def func(self):
    #     print("func")

    def db_connect(self):
        self.db = pymysql.connect(host='localhost',
                             user='root',
                             password='123',
                             port=3306,
                             database='zxfpydatabases')

    def inser_row(self, row, sid, name, sex, address):
        sid_item = QTableWidgetItem(sid)
        name_item = QTableWidgetItem(name)
        sex_item = QTableWidgetItem(sex)
        address_item = QTableWidgetItem(address)
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, sid_item)
        self.tableWidget.setItem(row, 1, name_item)
        self.tableWidget.setItem(row, 2, sex_item)
        self.tableWidget.setItem(row, 3, address_item)

    @pyqtSlot()
    def on_button_load_clicked(self):
        if self.button_save.isEnabled():
            r = QMessageBox.warning(self, "警告", "是否覆盖当前表格数据", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.No:
                return
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        self.db_connect()
        cursor = self.db.cursor()
        sql = "select * from my_student;"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for (sid, name, sex,address) in results:
                print(sid, name, sex, address)
                row = self.tableWidget.rowCount()
                # print(row)
                self.inser_row(row, sid, name, sex, address)
                data[sid] = [name, sex, address]
        except:
            print("unable to fetch data")

        self.db.close()
        self.button_save.setEnabled(True)
        print("load")

    @pyqtSlot()
    def on_button_add_clicked(self):
        di = inputDialog()
        ok = di.exec_()
        if not ok:
            return
        name = di.line_name.text()
        sid = di.line_id.text()
        sex = di.line_sex.text()
        address = di.line_address.text()
        print(name,sid)
        print(type(address))
        data[sid] = [name, sex, address]
        self.inser_row(self.tableWidget.rowCount(), sid, name, sex, address)
        print(data)
        print("add")
        # self.tableWidget.insertRow(self.tableWidget.rowCount()-1)
        self.button_save.setEnabled(True)


    @pyqtSlot()
    def on_button_save_clicked(self):
        print(data)
        self.db_connect()
        cursor = self.db.cursor()
        try:
            sql = "delete from my_student;"
            cursor.execute(sql)
            # self.db.commit()
            for key, value in data.items():
                sql = "insert into my_student(sid,name,sex,address) values('{sid}','{name}','{sex}','{address}');".format(sid=key, name=value[0], sex=value[1], address=value[2])
                print(sql)
                cursor.execute(sql)
            self.db.commit()
            self.db.close()
            print("save")
            self.button_save.setEnabled(False)
        except:
            QMessageBox.critical(self, "错误", "数据格式有误，请检查")


    @pyqtSlot()
    def on_button_clear_clicked(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        data.clear()
        self.line_id.clear()
        self.button_save.setEnabled(True)

    @pyqtSlot()
    def on_button_search_clicked(self):
        # self.close()
        # return
        sid = self.line_id.text()
        if not sid:
            QMessageBox.critical(self, "警告", "请输入一个学号！")
            return
        print(sid)
        if sid in data:
            search = INFO(sid)
            search.exec_()
            # print("search")
        else:
            QMessageBox.critical(self, "错误", "该学号不存在！")


    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemActivated(self, item):
        """
        按住Enter键时，当前选中的单元格向下
        """
        row = self.tableWidget.row(item)
        column = self.tableWidget.column(item)
        totalrow = self.tableWidget.rowCount()

        if row + 1 < totalrow:
            row = self.tableWidget.row(item) + 1
            self.tableWidget.setCurrentCell(row, column)
        elif row + 2 == totalrow:
            row = totalrow - 1
            self.tableWidget.setCurrentCell(row, column)

    @pyqtSlot(int, int)
    def on_tableWidget_cellDoubleClicked(self, row, column):
        id = self.tableWidget.item(row, 0).text()
        di = inputDialog(sid=id)
        ok = di.exec_()
        if not ok:
            return
        name = di.line_name.text()
        sid = di.line_id.text()
        sex = di.line_sex.text()
        address = di.line_address.text()
        print("before:", id)
        print("after:", sid)
        self.tableWidget.item(row, 0).setText(sid)
        self.tableWidget.item(row, 1).setText(name)
        self.tableWidget.item(row, 2).setText(sex)
        self.tableWidget.item(row, 3).setText(address)
        data[sid] = [name, sex, address]
        if id != sid:
            del data[id]
        self.button_save.setEnabled(True)


    def closeEvent(self, event):
        if self.button_save.isEnabled():
            r = QMessageBox.warning(self, "警告", "你还有操作没保存，现在保存下？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.No:
                event.accept()
            else:
                event.ignore()

    def context_menu(self,pos):
        pop_menu = QMenu()
        change_new_event = pop_menu.addAction("修改行")
        delete_event = pop_menu.addAction("删除行")
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))

        if action == change_new_event:
            item = self.tableWidget.selectedItems()
            row = item[0].row()
            id = self.tableWidget.item(row, 0).text()
            di = inputDialog(sid=id)
            ok = di.exec_()
            if not ok:
                return
            name = di.line_name.text()
            sid = di.line_id.text()
            sex = di.line_sex.text()
            address = di.line_address.text()
            print("before:",id)
            print("after:",sid)
            self.tableWidget.item(row, 0).setText(sid)
            self.tableWidget.item(row, 1).setText(name)
            self.tableWidget.item(row, 2).setText(sex)
            self.tableWidget.item(row, 3).setText(address)
            data[sid] = [name, sex, address]
            if id != sid:
                del data[id]
            self.button_save.setEnabled(True)
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
            self.button_save.setEnabled(True)


    # def contextMenuEvent(self, event):
    #     pmenu = QMenu(self)
    #     pDeleteAct = QAction("删除行", self.tableWidget)
    #     pmenu.addAction(pDeleteAct)
    #     pDeleteAct.triggered.connect(self.deleterows)
    #     pmenu.popup(self.mapToGlobal(event.pos()))
    #
    # def deleterows(self):
    #     """
    #     删除行
    #     """
    #     r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if r == QMessageBox.Yes:
    #         pass


class inputDialog(QDialog, Ui_Dialog_input):
    def __init__(self, sid=None):
        super(inputDialog, self).__init__()
        self.setupUi(self)
        self.sid = sid
        self.buttonBox.accepted.connect(self.check)

        if sid:
            self.line_id.setText(sid)
            self.line_name.setText(data[sid][0])
            self.line_sex.setText(data[sid][1])
            self.line_address.setText(data[sid][2])


    def check(self):
        sid = self.line_id.text()
        name = self.line_name.text()
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
        # print('miss')


class INFO(QDialog, Ui_Dialog_info):
    def __init__(self, id: str):
        super(INFO, self).__init__()
        self.setupUi(self)
        self.line_id.setText(id)
        self.line_name.setText(data[id][0])
        self.line_sex.setText(data[id][1])
        self.line_address.setText(data[id][2])

    @pyqtSlot()
    def on_button_confirm_clicked(self):
        # print(1)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
