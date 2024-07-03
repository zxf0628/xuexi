import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from Text_analysis.Gui.ui import Myui as file_ui
from Tcp.Gui.ui import Myui as tcp_ui
from Mysql.Gui.sql_ui_v2 import Myui as mysql_ui2
from Mysql.Gui.sql_ui import Myui as mysql_ui



class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True) # 设置标签可关闭
        self.tabCloseRequested.connect(self.closeTab) # 关联关闭标签的信号和槽

    def closeTab(self, index):
        if self.count() > 1: # 至少保留一个标签页
            self.removeTab(index)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Tab Widget Example")
        self.setGeometry(300, 200, 600, 400)

        # 创建QTabWidget对象
        self.tab_widget = TabWidget()
        self.setCentralWidget(self.tab_widget)

        # 创建两个UI界面类的实例
        self.page1 = file_ui()
        self.page2 = tcp_ui()
        self.page3 = mysql_ui2()

        # 将UI界面类的实例作为选项卡添加到QTabWidget中
        self.tab_widget.addTab(self.page1, "Text_analysis")
        self.tab_widget.addTab(self.page2, "通信")
        self.tab_widget.addTab(self.page3, "数据库")

        # vbox = QVBoxLayout()
        # vbox.addWidget(self.tab_widget)
        # self.setLayout(vbox)

        # 连接tabBarClicked信号到槽函数
        self.tab_widget.currentChanged.connect(self.tab_clicked)

    def tab_clicked(self, index):
        # 在槽函数中根据当前选中的标签来显示对应的UI界面
        if index == 0:
            self.page1.show_ui()
            # self.page2.hide()
        elif index == 1:
            self.page2.show_ui()
            # self.page1.hide()
        elif index == 2:
            self.page3.show_ui()


    def tabChanged(self, index):
        print('Tab Changed:', index)


if __name__  == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())