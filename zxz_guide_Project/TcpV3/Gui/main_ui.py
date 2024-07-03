import socket

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TcpMyui(QWidget):
    def __init__(self):
        super(TcpMyui, self).__init__()

    # 将每个盒子内写的控件 拼接到主界面上
    def join_ui(self):
        self.Global_layout = QVBoxLayout()  # 全局布置器

        self.initrow_ip()  # IP输入栏
        self.initrow_port()  # 端口输入栏
        self.initrow_host_name()  # 本机用户名输入栏
        self.initrow_select_function()  # 客户端与服务端的端口选择
        self.initrow_keystroke_middle()  # 中间部分按键
        self.initrow_edit()  # 编译文本
        self.initrow_keystroke_bottom()  # 底部按键

        self.statusBar = QStatusBar()
        self.Global_layout.addWidget(self.statusBar)

        self.set_control_size()

    # 运行主界面
    def set_show_ui(self):
        self.join_ui()

        self.setLayout(self.Global_layout)
        self.setWindowTitle("TCP通信")
        self.setFixedSize(QSize(460, 500))

    # 设置ui界面上，文本输入框的 宽高
    def set_control_size(self):
        self.set_QlineEdit_control_size(self.Ledit_ip)
        self.set_QlineEdit_control_size(self.Ledit_port)
        self.set_QlineEdit_control_size(self.Ledit_client_num)
        self.set_QlineEdit_control_size(self.Ledit_host_name)
        self.set_QlineEdit_control_size(self.Ledit_input,440)

    def set_QlineEdit_control_size(self,control,width=110,height=20):
        control.setFixedSize(width,height)


    def initrow_ip(self):
        self.Ledit_ip = QLineEdit()
        self.Ledit_ip.setInputMask("000.000.000.000;")
        self.Button_get_host = QPushButton("获得本机IP")  # 点击直接获得本机IP

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Server IP:  "))
        row1.addWidget(self.Ledit_ip)
        row1.addWidget(self.Button_get_host)
        row1.addStretch()

        self.Global_layout.addLayout(row1)

    def initrow_port(self):
        self.Ledit_port = QLineEdit()
        self.Ledit_port.setPlaceholderText("9999")

        self.Ledit_client_num = QLineEdit()
        self.Ledit_client_num.setPlaceholderText("5")

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Server prot:"))
        row2.addWidget(self.Ledit_port)
        row2.addWidget(QLabel("服务端接受连接上限:"))
        row2.addWidget(self.Ledit_client_num)
        row2.addStretch()
        self.Global_layout.addLayout(row2)

    def initrow_host_name(self):
        self.Ledit_host_name = QLineEdit()
        self.Ledit_host_name.setPlaceholderText(socket.gethostname())
        row_host_name = QHBoxLayout()
        row_host_name.addWidget(QLabel("Host name:  "))
        row_host_name.addWidget(self.Ledit_host_name)
        row_host_name.addStretch()
        self.Global_layout.addLayout(row_host_name)

    def initrow_select_function(self):
        self.Button_server = QRadioButton("Server")  # 选择为服务器
        self.Button_server.setChecked(True)
        self.Button_client = QRadioButton("Client")  # 选择为客户端
        row_select = QHBoxLayout()
        row_select.addWidget(self.Button_server)
        row_select.addWidget(self.Button_client)
        row_select.addStretch()
        self.Global_layout.addLayout(row_select)

    def initrow_keystroke_middle(self):
        self.Button_connect_server = QPushButton("连接服务器")  # 连接服务器按钮
        self.Button_connect_server.setEnabled(False)
        self.Button_build_server = QPushButton("建立服务器")  # 建立服务器按钮
        self.Button_quit = QPushButton("退出")  # 退出按钮

        row_keystroke = QVBoxLayout()
        row_keystroke.addWidget(self.Button_connect_server)
        row_keystroke.addWidget(self.Button_build_server)
        row_keystroke.addWidget(self.Button_quit)
        self.Global_layout.addLayout(row_keystroke)

    def initrow_edit(self):
        self.Tedit_chat = QTextEdit()  # 聊天对话框
        self.Ledit_input = QLineEdit()  # 输入框
        row_edit = QVBoxLayout()
        row_edit.addWidget(self.Tedit_chat)
        row_edit.addWidget(self.Ledit_input)
        self.Global_layout.addLayout(row_edit)

    def initrow_keystroke_bottom(self):
        self.Button_send = QPushButton("发送")  # 发送按钮
        self.Button_clear = QPushButton("清空")  # 清空按钮
        self.Button_chatting_records = QPushButton("导出聊天记录")

        self.Button_get_friend_list = QPushButton("获取好友列表")
        self.Button_get_friend_list.setEnabled(False)
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