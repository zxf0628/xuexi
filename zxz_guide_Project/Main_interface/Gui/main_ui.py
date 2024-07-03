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

# class Main_Ui(QWidget):
#     def __init__(self):
#         super(Main_Ui, self).__init__()
#         self.row_button()
#         self.show_ui()
#
#     def row_button(self):
#         self.button_read_data = QPushButton("读取LOG数据")
#         self.button_tcp = QPushButton("TCP通信")
#         self.row = QHBoxLayout()
#         self.row.addWidget(self.button_read_data)
#         self.row.addWidget(self.button_tcp)
#
#     def join_ui(self):
#         pass
#
#     def show_ui(self):
#         self.win = QWidget()
#         self.win.setLayout(self.row)
#         self.win.setFixedSize(QSize(600,300))
#         self.win.setWindowTitle("武功谱")
#         self.win.show()
#
# if __name__  == "__main__":
#     app = QApplication(sys.argv)
#     f_ui = file_ui()
#     t_ui = tcp_ui()
#     main_ui = Main_Ui()
#     main_ui.button_read_data.clicked.connect(f_ui.show_ui)
#     main_ui.button_tcp.clicked.connect(t_ui.show_ui)
#     sys.exit(app.exec_())


# page1 = file_ui()
# page2 = tcp_ui()
# page3 = mysql_ui()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tab Widget Example")
        self.setGeometry(300, 200, 600, 400)

        # 创建QTabWidget对象
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # 创建两个UI界面类的实例
        self.page1 = file_ui()
        self.page2 = tcp_ui()
        self.page3 = mysql_ui()

        # 将UI界面类的实例作为选项卡添加到QTabWidget中
        self.tab_widget.addTab(self.page1, "Text_analysis")
        self.tab_widget.addTab(self.page2, "通信")
        self.tab_widget.addTab(self.page3, "数据库")

        # 连接tabBarClicked信号到槽函数
        # self.tab_widget.tabBarClicked.connect(self.tab_clicked)

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



if __name__  == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())