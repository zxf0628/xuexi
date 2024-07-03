import socket
from PyQt5.QtCore import QThread, pyqtSignal
from TcpV3.data_centers.data_transfer import Data_Center
from TcpV3.signal_centers.signal_transfer import Signal_Center


class Client:
    def __init__(self, host_name):
        self.data_center = Data_Center()
        self.signal_center = Signal_Center()
        self.host_name = host_name

        self.buildSocket()

    # 创建套接字
    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buildClient()

    # 创建客户端
    def buildClient(self):
        print("Client->buildClient->")
        self.client = ClientThread(self.socket, self.host_name)

        self.client._flag.connect(self.sin_get_flag)

        self.ip = self.data_center.get_ip()
        self.port = self.data_center.get_port()
        if self.client.connectServer(self.ip, self.port):

            # 发送一个自定义的操作 让服务端 更新ID为hostname
            id_join = "@@@".join(["更新名称", self.host_name])
            self.socket.send(id_join.encode("utf-8"))

            self.client.start()
        else:
            self.signal_center.trigger_StatusBar_signal("客户端线程连接服务端失败")

    # 关闭客户端线程
    def closeThread(self):
        print("Client->closeThread->")
        self.client.runflag = False
        self.socket.close()

    # 槽函数，修改线程的连接状态
    def sin_get_flag(self, flag):
        print("Client->sin_get_flag->{}".format(flag))
        if flag == "connect":
            self.signal_center.trigger_StatusBar_signal("连接成功！！！")
        else:
            self.client.runflag = False

    # 客户端向服务端发送消息
    def send_to_server(self, text):
        print("Client->send_to_server->{}".format(text))
        target = self.data_center.get_select_target()
        data_join = "@@@".join([target, text])
        try:
            print("Client->send_to_server->通过套接字要发的消息内容{}".format(data_join))
            self.socket.send(data_join.encode("utf-8"))
        except Exception as reason:
            print("异常：Client->send_to_server->{}".format(reason))
            self.signal_center.trigger_StatusBar_signal("发消息失败")
            self.sin_get_flag("disconnect")

    # 主流程界面触发的控件点击"发送消息"函数
    def btnsend(self, text):
        print("Client->btnsend->{}".format(text))
        self.send_to_server(text)

    # 主流程界面触发的控件点击"获取在线好友"函数
    def get_target(self, text):
        print("Client->get_target->{}".format(text))
        try:
            self.socket.send(text.encode("utf-8"))
        except Exception as reason:
            print("异常：Client->get_target->{}".format(reason))
            self.signal_center.trigger_StatusBar_signal("获取在线好友失败")
            self.sin_get_flag("disconnect")


class ClientThread(QThread):
    _flag = pyqtSignal(str)

    def __init__(self, clientsocket, host_name):
        super(ClientThread, self).__init__()
        self.signal_center = Signal_Center()

        self.clientsocket = clientsocket
        self.host_name = host_name
        self.runflag = True

    def run(self):
        print("ClientThread->run->")
        while self.runflag:
            try:
                recv_data = self.clientsocket.recv(1024).decode("utf-8")
                self.recv_message_select_whither(recv_data)
            except Exception as reason:
                print("异常：ClientThread->run->{}".format(reason))
                self.signal_center.trigger_StatusBar_signal("客户端线程循环接收消息函数异常：" + str(reason))
                self.sin_send_flag(1)
                break

    # socket对象客户端连接服务端
    def connectServer(self, ip, port):
        print("ClientThread->connectServer->{}".format(str(ip) + str(port)))
        try:
            self.clientsocket.connect((ip, port))
            self.sin_send_flag(0)
            return True
        except Exception as reason:
            print("异常：ClientThread->connectServer->{}".format(reason))
            self.signal_center.trigger_StatusBar_signal("客户端线程连接服务端函数异常：" + str(reason))
            self.sin_send_flag(1)
            return

    # 触发信号，通过在客户端类内修改客户端的连接状态
    def sin_send_flag(self, flagindex):
        print("ClientThread->sin_send_flag->{}".format(flagindex))
        connectList = ["connect", "disconnect"]
        self._flag.emit(connectList[flagindex])

    # 根据收到消息的前缀进行判断操作
    def recv_message_select_whither(self, recv_data):
        print("ClientThread->recv_message_select_whither->{}".format(recv_data))
        try:
            recv_datas = recv_data.split("@@@")
            if recv_datas[0] == "服务端:返回在线好友":
                targets = recv_datas[1].split(",")
                targets.append("服务端")
                print("ClientThread->recv_message_select_whither->处理后列表{}".format(targets))
                if "广播" in targets : targets.remove("广播")
                self.signal_center.trigger_ComboBox_select_target(str(targets))
                self.signal_center.trigger_Tedit_chat(recv_data)

            elif recv_datas[0] == "服务端:服务端连接数量达到上限":
                self.signal_center.trigger_QMessageBox("已达到服务端连接数量上限，连接无效")
                print("ClientThread->recv_message_select_whither->提示服务端连接数量已上限,id号：{}".format(self.host_name))

            else:
                print("ClientThread->recv_message_select_whither->正常接受数据，未做其他处理：{}".format(recv_data))
                self.signal_center.trigger_Tedit_chat(recv_data)
        except Exception as reason:
            print("异常：ClientThread->recv_message_select_whither->{}".format(reason))
            self.sin_send_flag(1)