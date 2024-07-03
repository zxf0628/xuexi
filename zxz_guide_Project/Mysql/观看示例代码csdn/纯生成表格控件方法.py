from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class MyWin(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 TableWidget"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 380
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.creatingTables()

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.table)
        self.setLayout(self.vBoxLayout)

        self.show()

    def creatingTables(self):
        # 创建 QTablewWidget对象，设置表头及参数
        self.table = QTableWidget(4, 3, self)
        self.table.setShowGrid(True)
        self.table.setHorizontalHeaderLabels(('姓名', '邮件', '电话'))
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        # 表格内容
        self.table.setItem(0, 0, QTableWidgetItem("张飞"))
        self.table.setItem(0, 1, QTableWidgetItem("zhangfei@example.com"))
        self.table.setItem(0, 2, QTableWidgetItem("021-3233288"))

        self.table.setItem(1, 0, QTableWidgetItem("李军"))
        self.table.setItem(1, 1, QTableWidgetItem("lijun@example.com"))
        self.table.setItem(1, 2, QTableWidgetItem("021-34334433"))

        self.table.setItem(2, 0, QTableWidgetItem("王小乙"))
        self.table.setItem(2, 1, QTableWidgetItem("wangxiaoyi@example.com"))
        self.table.setItem(2, 2, QTableWidgetItem("2232324"))

        self.table.setItem(3, 0, QTableWidgetItem("赵无忌"))
        self.table.setItem(3, 1, QTableWidgetItem("zhaowuji@example.com"))
        item = QTableWidgetItem()
        item.setData(Qt.EditRole, 55555555)
        self.table.setItem(3, 2, item)

        # 添加1条新记录
        row_5 = ['钱晓芬', "xiaofengz@example.com", "12343445"]
        row_6 = ['孙涛', 'suntao@example.com', '88888888']
        self.addTableRow(self.table, row_5)
        self.addTableRow(self.table, row_6)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        self.table.cellDoubleClicked.connect(self.table_double_clicked)

    def addTableRow(self, table, row_data):
        # 功能： 在末尾添加新行
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
        print(f"Added one row: {row_data}")
        print(f"totally, {row + 1} rows")

    def table_double_clicked(self, row, col):
        # 打印选中单元格的内容
        print(f" Value of cell ({row},{col}) is {self.table.item(row, col).text()}  ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWin()
    sys.exit(app.exec())
