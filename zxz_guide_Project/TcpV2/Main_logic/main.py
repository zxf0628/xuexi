import sys
from PyQt5.QtWidgets import QApplication

from TcpV2.Gui.main_ui import TcpMyui
from Universal_Methods.Universal_Method import Common_Method
from TcpV2.communication.Server import Server
from TcpV2.communication.Client import Client
from TcpV2.data_centers.data_transfer import Data_Center
from TcpV2.signal_centers.signal_transfer import Signal_Center


class Tcplogic(TcpMyui):
    def __init__(self):
        super(Tcplogic, self).__init__()
        self.join_ui()
        self.set_show_ui()
        self.data_center = Data_Center()
        self.signal_center = Signal_Center()

        self.initialize_ui_butthon_connect_to_fun()
        self.initialize_Singal_connect_to_groove_fun()
        self.initialize_ui_data_update_to_data_transfer_connect_singal()

        self.pc = None
        self.server_host_names = []

    # 初始化 将ui上控件绑定对应触发方法
    def initialize_ui_butthon_connect_to_fun(self):
        self.Button_get_host.clicked.connect(self.getHostIP)
        self.Button_server.toggled.connect(self.radiobtnChange)
        self.Button_connect_server.clicked.connect(self.setClient)
        self.Button_build_server.clicked.connect(self.setServer)
        self.Button_quit.clicked.connect(self.quit)
        self.Button_send.clicked.connect(self.sendInfo)
        self.Button_clear.clicked.connect(lambda: self.Ledit_input.clear())
        self.Button_chatting_records.clicked.connect(self.derive_chatting_records)
        self.Button_get_friend_list.clicked.connect(self.get_friend)

    # 信号中心的信号绑定到槽函数
    def initialize_Singal_connect_to_groove_fun(self):
        self.signal_center._Tedit_chat.connect(self.sin_get_text)
        self.signal_center._StatusBar_signal.connect(self.sin_get_message)
        self.signal_center._ComboBox_select_target.connect(self.sin_get_targets)

    # UI控件自带信号，一旦修改数据，触发更新数据
    def initialize_ui_data_update_to_data_transfer_connect_singal(self):
        self.Ledit_ip.textChanged.connect(self.ui_data_to_data_transfer)
        self.Ledit_port.textChanged.connect(self.ui_data_to_data_transfer)
        self.Ledit_client_num.textChanged.connect(self.ui_data_to_data_transfer)
        self.select_target.activated.connect(self.ui_data_to_data_transfer)

    def ui_data_to_data_transfer(self):
        ip = self.Ledit_ip.text()
        port = self.Ledit_port.text()
        client_num = self.Ledit_client_num.text()
        target = self.select_target.currentText()
        if ip: self.data_center.set_ip(ip)
        if port: self.data_center.set_port(port)
        if client_num: self.data_center.set_connect_num(client_num)
        if target: self.data_center.set_select_target(target)

    # 静态的根据UI选择是服务端还是客户端，进行置灰相应控件按钮
    def radiobtnChange(self, status):
        if status:
            self.Button_connect_server.setEnabled(False)
            self.Button_build_server.setEnabled(True)
            self.Button_get_friend_list.setEnabled(False)
        else:
            self.Button_connect_server.setEnabled(True)
            self.Button_build_server.setEnabled(False)
            self.Button_get_friend_list.setEnabled(True)

    # 获取本机的IP地址
    def getHostIP(self):
        hostip = Common_Method.getHostIP()
        self.Ledit_ip.setText(hostip)

    # 退出Qt界面，关闭线程
    def quit(self):
        if self.pc is not None:
            self.pc.closeThread()
        self.close()

    # 选择实例为服务端
    def setServer(self):
        host_name = self.Ledit_host_name.text()
        port = self.Ledit_port.text()
        ip = self.Ledit_ip.text()
        connect_num = self.Ledit_client_num.text()
        if host_name == "": host_name = "服务管理员"
        if port == "": port = 9999
        if ip == "...": ip = "127.0.0.1"
        if connect_num == "": connect_num = "5"
        self.data_center.set_ip(ip)
        self.data_center.set_port(port)
        self.data_center.set_host_name(host_name)
        self.data_center.set_connect_num(connect_num)

        self.pc = Server()

    # 选择实例为客户端
    def setClient(self):
        port = self.Ledit_port.text()
        ip = self.Ledit_ip.text()
        host_name = self.Ledit_host_name.text()
        if port == "": port = 9999
        if ip == "...": ip = "127.0.0.1"
        if host_name == "":
            self.sin_get_message("必须填写host_name")
            return
        elif host_name in self.server_host_names:
            self.Ledit_host_name.clear()
            self.sin_get_message("host_name已存在请从命名")
            return
        self.server_host_names.append(host_name)

        self.data_center.set_ip(ip)
        self.data_center.set_port(port)

        self.pc = Client(host_name)

    # 发送消息按钮
    def sendInfo(self):

        if self.pc == None:
            self.statusBar.showMessage("没有客户端连接")
        else:
            info = self.Ledit_input.text()
            if info != "":
                print("Tcplogic->sendInfo->{}".format(info))
                self.pc.btnsend(info)
            else:
                self.statusBar.showMessage("输入的发送内容为空")

    # 导出聊天记录
    def derive_chatting_records(self):
        content = self.Tedit_chat.toPlainText()
        curr_datetime_str = Common_Method.now_time_str()
        with open("./{}.txt".format(curr_datetime_str), "a", encoding="utf-8") as f:
            f.write(content)

    # 服务端获取所有在线的客户端好友
    def get_friend(self):
        text_full = "获取在线好友@@@1"
        self.pc.get_target(text_full)

    # 触发信号的槽函数
    def sin_get_text(self, text):
        print("主界面触发槽函数 Tcplogic->sin_get_text->{}".format(text))
        self.Tedit_chat.append(text)

    def sin_get_message(self, hint):
        print("主界面触发槽函数 Tcplogic->sin_get_message->{}".format(hint))
        self.statusBar.showMessage(hint)

    def sin_get_targets(self, target_list):
        print("主界面触发槽函数 Tcplogic->sin_get_targets->{}".format(target_list))
        self.select_target.clear()
        target_lists = eval(target_list)
        target_lists.append("广播")
        self.select_target.addItems(target_lists)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Tcplogic()
    ui.show()
    sys.exit(app.exec_())
