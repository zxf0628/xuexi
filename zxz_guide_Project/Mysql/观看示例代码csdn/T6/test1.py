#QTableWidget 控件使用
from PyQt5.QtWidgets import  QTableView,QAbstractItemView,QHeaderView,QTableWidget, QTableWidgetItem, QMessageBox,QListWidget,QListWidgetItem, QStatusBar,  QMenuBar,QMenu,QAction,QLineEdit,QStyle,QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QMainWindow,QGridLayout,QLabel
from PyQt5.QtGui import QIcon,QPixmap,QStandardItem,QStandardItemModel,QCursor
from PyQt5.QtCore import QStringListModel, QAbstractListModel, QModelIndex, QSize, Qt, pyqtSlot, QMetaObject
import sys

class WindowClass(QWidget):

    def __init__(self,parent=None):

        super(WindowClass, self).__init__(parent)
        self.resize(400,400)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(2)
        self.nums = 3

        newItem = QTableWidgetItem("新单元格")
        self.tableWidget.setItem(0,1,newItem)

        self.btn = QPushButton("btn",self)
        self.btn.move(200,200)
        self.btn.setObjectName("btn")
        # btn.clicked.connect(self.func)
        QMetaObject.connectSlotsByName(self)
        self.show()

    @pyqtSlot()
    def on_btn_clicked(self):
        # print(self.tableWidget.rowCount())
        # self.tableWidget.insertRow(self.nums)
        # self.nums += 1
        # print(self.tableWidget.rowCount())
        print(self.tableWidget.currentRow())



    def closeEvent(self, event):

        r = QMessageBox.warning(self, "注意", "你是不是没有保存啊，现在保存下？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if r == QMessageBox.No:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemActivated(self, item):
        row = self.tableWidget.row(item)
        column = self.tableWidget.column(item)
        totalrow = self.tableWidget.rowCount()
        if row + 1 < totalrow:
            row = self.tableWidget.row(item) + 1
            self.tableWidget.setCurrentCell(row, column)
        elif row + 2 == totalrow:
            self.tableWidget.setCurrentCell(totalrow, column)


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())