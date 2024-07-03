import sys


from PyQt5.QtWidgets import *
from TcpV3.Main_logic.main import Tcplogic
from MysqlV2.Main_logic.MysqlLogic import MysqlLogic
from Text_analysisV2.Main_logic.Text_analysis_logic import Text_analysis_logic


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        # 创建QTabWidget对象
        self.tab_widget = QTabWidget()

        # 创建UI界面类的实例
        self.page1 = Text_analysis_logic()
        self.page2 = Tcplogic()
        self.page3 = MysqlLogic()


        # 将UI界面类的实例作为选项卡添加到QTabWidget中
        self.tab_widget.addTab(self.page1, "文本解析")
        self.tab_widget.addTab(self.page2, "通信")
        self.tab_widget.addTab(self.page3, "数据库")
        # 设置默认选中索引
        self.tab_widget.setCurrentIndex(0)

        # 连接控件自带索引发生改变时触发的信号 绑定到槽函数
        self.tab_widget.currentChanged.connect(self.onTabChanged)

        # 将tab界面放入布局盒子中，将界面在设置为盒子
        vbox = QVBoxLayout()
        vbox.addWidget(self.tab_widget)
        self.setLayout(vbox)

        # 设置弹框名字，设置大小
        self.setWindowTitle("Tab Widget Example")
        self.setGeometry(200, 200, 600, 400)





    def onTabChanged(self,index):
        print("onTabChanged index = " + str(index))
        self.tab_widget.setTabVisible(index,True)





if __name__  == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())