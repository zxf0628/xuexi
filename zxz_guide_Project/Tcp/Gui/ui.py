import os
import sys
import socket
import datetime

# 1. 获取基于该文件的上上级目录，为：*\Tcp，os.path.dirname一个嵌套为一级
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Tcp.communication import Server, Client
from Universal_Methods.Universal_Method import Common_Method


class Myui(QWidget):
    def __init__(self):
        super(Myui, self).__init__()
        self.join_ui()
        self.show_ui()

    def join_ui(self):
        self.Global_layout = QVBoxLayout()  # 全局布置器

        self.initrow_ip()  # IP输入栏
        self.initrow_port()  # 端口输入栏
        self.initrow_host_name()  # 本机用户名输入栏
        self.initrow_select()  # 客户端与服务端的端口选择
        self.initrow_keystroke_middle()  # 中间部分按键
        self.initrow_edit()  # 编译文本
        self.initrow_keystroke_bottom()  # 底部按键

        self.statusBar = QStatusBar()
        self.Global_layout.addWidget(self.statusBar)

    # 运行主界面
    def show_ui(self):

        self.setLayout(self.Global_layout)
        self.setWindowTitle("TCP通信")
        self.setFixedSize(QSize(460, 500))
        # self.my_ui.show()


    def initrow_ip(self):
        self.Ledit_ip = QLineEdit()
        self.Ledit_ip.setInputMask("000.000.000.000;")
        self.Ledit_ip.setMinimumWidth(50)
        self.Ledit_ip.setMinimumHeight(10)
        self.Button_get_host = QPushButton("获得本机IP")  # 点击直接获得本机IP
        self.Button_get_host.clicked.connect(self.getHostIP)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Server IP:  "))
        row1.addWidget(self.Ledit_ip)
        row1.addStretch()
        row1.addWidget(self.Button_get_host)

        self.Global_layout.addLayout(row1)

    def initrow_port(self):
        self.Ledit_port = QLineEdit()
        self.Ledit_port.setMinimumWidth(50)
        self.Ledit_port.setMinimumHeight(10)
        self.Ledit_port.setPlaceholderText("9999")
        self.Ledit_client_num = QLineEdit()
        self.Ledit_client_num.setPlaceholderText(str(5))

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Server prot:"))
        row2.addWidget(self.Ledit_port)
        row2.addWidget(QLabel("最多连接数："))
        row2.addWidget(self.Ledit_client_num)
        row2.addStretch(2)
        self.Global_layout.addLayout(row2)

    def initrow_host_name(self):
        self.Ledit_host_name = QLineEdit()
        self.Ledit_host_name.setMinimumWidth(50)
        self.Ledit_host_name.setMinimumHeight(10)
        self.Ledit_host_name.setPlaceholderText(socket.gethostname())
        row_host_name = QHBoxLayout()
        row_host_name.addWidget(QLabel("Host name:  "))
        row_host_name.addWidget(self.Ledit_host_name)
        row_host_name.addStretch(2)
        self.Global_layout.addLayout(row_host_name)

    def initrow_select(self):
        self.Button_server = QRadioButton("Server")  # 选择为服务器
        self.Button_server.setChecked(True)
        self.Button_server.toggled.connect(self.radiobtnChange)
        self.Button_client = QRadioButton("Client")  # 选择为客户端
        row_select = QHBoxLayout()
        row_select.addWidget(self.Button_server)
        row_select.addWidget(self.Button_client)
        row_select.addStretch()
        self.Global_layout.addLayout(row_select)

    def initrow_keystroke_middle(self):
        self.Button_connect_server = QPushButton("连接服务器")  # 连接服务器按钮
        self.Button_connect_server.clicked.connect(self.setClient)
        self.Button_connect_server.setEnabled(False)
        self.Button_build_Server = QPushButton("建立服务器")  # 建立服务器按钮
        self.Button_build_Server.clicked.connect(self.setServer)
        self.Button_quit = QPushButton("退出")  # 退出按钮
        self.Button_quit.clicked.connect(self.quit)
        row_keystroke = QVBoxLayout()
        row_keystroke.addWidget(self.Button_connect_server)
        row_keystroke.addWidget(self.Button_build_Server)
        row_keystroke.addWidget(self.Button_quit)
        self.Global_layout.addLayout(row_keystroke)

    def initrow_edit(self):
        self.Tedit_chat = QTextEdit()  # 聊天对话框
        self.Tedit_chat.setMinimumWidth(50)
        self.Tedit_chat.setMinimumHeight(20)
        self.Ledit_input = QLineEdit()  # 输入框
        self.Ledit_input.setMinimumWidth(50)
        self.Ledit_input.setMinimumHeight(10)
        row_edit = QVBoxLayout()
        row_edit.addWidget(self.Tedit_chat)
        row_edit.addWidget(self.Ledit_input)
        self.Global_layout.addLayout(row_edit)

    def initrow_keystroke_bottom(self):
        self.Button_send = QPushButton("发送")  # 发送按钮
        self.Button_send.clicked.connect(self.sendInfo)  # 向服务器发送信息(如果是服务器本身则广播)
        self.Button_clear = QPushButton("清空")  # 清空按钮
        self.Button_clear.clicked.connect(lambda: self.Ledit_input.clear())
        self.Button_chatting_records = QPushButton("导出聊天记录")
        self.Button_chatting_records.clicked.connect(self.derive)

        self.Button_get_friend_list = QPushButton("获取好友列表")
        self.Button_get_friend_list.setEnabled(False)
        self.Button_get_friend_list.clicked.connect(self.get_friend)

        self.select_target = QComboBox()

        row_keystroke_left = QHBoxLayout()
        row_keystroke_left.addStretch()
        row_keystroke_left.addWidget(self.Button_get_friend_list)
        row_keystroke_left.addWidget(QLabel("目标:"))
        row_keystroke_left.addWidget(self.select_target)
        row_keystroke_left.addWidget(self.Button_send)
        row_keystroke_left.addWidget(self.Button_clear)
        row_keystroke_left.addWidget(self.Button_chatting_records)
        row_keystroke_left.addStretch()
        self.Global_layout.addLayout(row_keystroke_left)

    # 获取本机IP
    def getHostIP(self):
        hostip = Common_Method.getHostIP()
        self.Ledit_ip.setText(hostip)

    # 静置函数 - 用于写事件函数-------------------------
    # 单选按钮切换函数
    def radiobtnChange(self, status):
        if status:
            self.Button_connect_server.setEnabled(False)
            self.Button_build_Server.setEnabled(True)
            self.Button_get_friend_list.setEnabled(False)
        else:
            self.Button_connect_server.setEnabled(True)
            self.Button_build_Server.setEnabled(False)
            self.Button_get_friend_list.setEnabled(True)

    # 设定本主机为服务器
    def setServer(self):
        host = self.Ledit_host_name.text()
        port = self.Ledit_port.text()
        ip = self.Ledit_ip.text()
        print(ip)
        if host == "": host = "服务管理员"  # 服务主机
        if port == "": port = 9999  # 默认端口
        if ip == "...": ip = "127.0.0.1"  # 默认IP
        self.pc = Server.Server(self, ip, host, int(port))

    # 设定本主机为客户端
    def setClient(self):
        host = self.Ledit_host_name.text()
        port = self.Ledit_port.text()
        ip = self.Ledit_ip.text()
        if host == "": host = "匿名用户"  # 匿名用户
        if port == "": port = 9999  # 默认端口
        if ip == "...": ip = "127.0.0.1"  # 默认IP
        self.pc = Client.Client(self, ip, host, int(port))

    # 发送消息
    def sendInfo(self):
        if self.pc == None:
            self.statusBar.showMessage("没有客户端连接")
        else:
            info = self.Ledit_input.text()
            if info != "":
                info = self.pc.host + ":\n" + info
                self.pc.btnsend(info)
            else:
                self.statusBar.showMessage("输入的发送内容为空")

    # 退出Qt界面
    def quit(self):
        if self.pc != None:
            self.pc.closeThread()
        self.my_ui.close()

    # 获得编译文本控件中内容
    def derive(self):
        content = self.Tedit_chat.toPlainText()
        curr_datetime = datetime.datetime.now()
        curr_datetime_str = curr_datetime.strftime("%Y,%m,%d,%H,%M")
        with open("./{}.txt".format(curr_datetime_str), "a", encoding="utf-8") as f:
            f.write(content)

    def get_friend(self):
        text_full = "获取在线好友@@@1"
        self.select_target.clear()
        self.pc.btnsend_c_to_c(text_full)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = Myui()
#     dialog.my_ui.show()
#     sys.exit(app.exec_())
