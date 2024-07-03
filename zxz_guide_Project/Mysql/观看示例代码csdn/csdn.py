from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QLineEdit, QMessageBox
import xlwt
import table001
import sys
import MySQLdb


class MyClass(QWidget, table001.Ui_Form):
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.My_Sql()

    def InitUi(self):
        self.setupUi(self)
        self.setWindowTitle("轨道检测")
        self.show()
        self.pushButton.clicked.connect(self.setBrowerPath)
        self.pushButton_2.clicked.connect(self.savefile)
        self._translate = QtCore.QCoreApplication.translate

    def Table_Data(self, i, j, data):

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(i, j, item)
        item = self.tableWidget.item(i, j)
        item.setText(self._translate("Form", str(data)))

    def My_Sql(self):  # 连接mysql数据库
        connection = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='imooc',
                                     charset='utf8')
        print('successfully connect')
        cur = connection.cursor()
        cur.execute('select * from new_table')  # 将数据从数据库中拿出来
        total = cur.fetchall()
        col_result = cur.description
        self.row = cur.rowcount  # 取得记录个数，用于设置表格的行数
        self.vol = len(total[0])  # 取得字段数，用于设置表格的列数
        col_result = list(col_result)
        a = 0
        self.tableWidget.setColumnCount(self.vol)
        self.tableWidget.setRowCount(self.row)
        for i in col_result:  # 设置表头信息，将mysql数据表中的表头信息拿出来，放进TableWidget中
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(a, item)
            item = self.tableWidget.horizontalHeaderItem(a)
            item.setText(self._translate("Form", i[0]))
            a = a + 1

        total = list(total)  # 将数据格式改为列表形式，其是将数据库中取出的数据整体改为列表形式
        for i in range(len(total)):  # 将相关的数据
            total[i] = list(total[i])  # 将获取的数据转为列表形式
        for i in range(self.row):
            for j in range(self.vol):
                self.Table_Data(i, j, total[i][j])

    def setBrowerPath(self):  # 选择文件夹进行存储
        download_path = QtWidgets.QFileDialog.getExistingDirectory(None, "浏览", "/home")
        self.lineEdit.setText(download_path)

    def savefile(self):
        print("hello")
        book = xlwt.Workbook()
        sheet = book.add_sheet('超限数据报表')
        for i in range(0, self.tableWidget.rowCount()):
            for j in range(0, self.tableWidget.columnCount()):
                try:
                    sheet.write(i, j, self.tableWidget.item(i, j).text())
                except:
                    continue
        if len(self.lineEdit_2.text()) < 1:
            QMessageBox.information(self.pushButton, ' ', '文件名不可为空', QMessageBox.Ok)
        else:
            try:
                book.save(self.lineEdit.text() + '/' + self.lineEdit_2.text() + '.xls')
                QApplication.instance().exit()

            except:
                QMessageBox.information(self.pushButton, ' ', '所选目录错误！', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mc = MyClass()
    sys.exit(app.exec_())
