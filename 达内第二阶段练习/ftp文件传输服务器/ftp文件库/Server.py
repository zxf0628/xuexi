import socket

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from TcpV3.data_centers.data_transfer import Data_Center
from TcpV3.signal_centers.signal_transfer import Signal_Center

Server_Dict = {}
Server_id = 1


def filtration_disconnect_flag_client():
    target_list = [i for i in Server_Dict.keys()]
    for client in Server_Dict:
        if Server_Dict[client].clientsocket is None:
            target_list.remove(client)
    return target_list


class Server(QObject):

    def __init__(self):
        super(Server, self).__init__()
        self.data_center = Data_Center()
        self.signal_center = Signal_Center()
        self.target_connect = None
        self.target_list = []
        self.buildSocket()

    # 创建套接字
    def buildSocket(self):
        print("Server->buildSocket->")
        ip = self.data_center.get_ip()
        port = self.data_center.get_port()
        connect_num = self.data_center.get_connect_num()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(int(connect_num))

        self.buildServer()

    # 创建服务端线程
    def buildServer(self):
        global Server_Dict
        global Server_id
        server = Server_Thread(self.socket, str(Server_id))
        Server_Dict[str(Server_id)] = server
        Server_id += 1
        print("Server->buildServer->全局变量Server_Dict：{}".format(Server_Dict))

        server._flag.connect(self.sin_get_flag)
        server._send_info_all.connect(self.send_info_to_all)
        server._send_info_c_to_c.connect(self.sin_get_send_c_to_c)
        server._update_server_id.connect(self.sin_update_server_id)
        server.start()

    # 发送消息功能 根据服务端选择的目标 进行是广播还是单独发送
    def send_info(self, text):
        print("Server->send_info->{}".format(text))
        self.target_connect = self.data_center.get_select_target()
        if self.target_connect == "广播" or self.target_connect == "":
            self.send_info_to_all(text)
        else:
            text = "@@@".join([self.target_connect, text])
            print("Server->send_info->发送到选择的目标拼接后消息:{}".format(text))
            self.send_info_to_target(text)

    def send_info_to_all(self, text):
        print("Server->send_info_to_all->{}".format(text))
        for client in Server_Dict:
            try:
                if Server_Dict[client].clientsocket is not None:
                    text_join = "服务端:" + text
                    Server_Dict[client].send_to_client(text_join)
                    print("Server->send_info_to_all 完成发送->{}".format(text))
            except Exception as reason:
                self.sin_get_flag("@@@".join([client, "disconnect"]))
                self.signal_center.trigger_StatusBar_signal("服务端向客户端广播消息失败")
                print("异常：Server->send_info_to_all->{}".format(reason))

    def send_info_to_target(self, text):
        print("Server->send_info_to_target->{}".format(text))
        try:
            if Server_Dict[self.target_connect].clientsocket is not None:
                text_join = "服务端：" + text
                Server_Dict[self.target_connect].send_to_client(text_join)
        except Exception as reason:
            self.sin_get_flag("@@@".join([self.target_connect, "disconnect"]))
            self.signal_center.trigger_StatusBar_signal("服务端向单个客户端发送消息失败")
            print("异常：Server->send_info_to_target->{}".format(reason))

    # ui界面点击发送按钮，触发的发送功能
    def btnsend(self, text):
        print("Server->btnsend->{}".format(text))
        self.signal_center.trigger_Tedit_chat(text)
        self.send_info(text)

    # 槽函数，客户端通过服务端转发给客户端消息，达到c_to_c
    def sin_get_send_c_to_c(self, text):
        print("Server->sin_get_send_c_to_c->{}".format(text))
        texts = text.split("@@@")
        data_join = " ".join([texts[0], texts[2]])
        try:
            if Server_Dict[texts[1]].clientsocket is not None:
                Server_Dict[texts[1]].send_to_client(data_join)
        except Exception as reason:
            self.sin_get_flag("@@@".join([texts[1], "disconnect"]))
            print("异常：Server->sin_get_send_c_to_c->{}".format(reason))

    # 根据触发的信号来管理，全局变量下客户端的runflag状态
    def sin_get_flag(self, flag):
        print("Server->sin_get_flag->{}".format(flag))
        global Server_Dict
        flags = flag.split("@@@")
        if flags[1] == "connect":
            self.buildServer()
        elif flags[1] == "disconnect":
            Server_Dict[flags[0]].runFlag = False
            print("Server->sin_get_flag->修改线程状态后 全局变量Server_Dict：{}".format(Server_Dict[flags[0]].runFlag))
            del Server_Dict[flags[0]]
            print("Server->sin_get_flag->修改线程状态并清除后 全局变量Server_Dict：{}".format(Server_Dict))
            self.to_ui_deposit_id()

    # 槽函数,根据接受的消息拆分，进行将原默认ID替换成为客户端输入的host_name
    def sin_update_server_id(self, old_and_new_id):
        print("Server->sin_update_server_id->{}".format(old_and_new_id))
        old_and_new_ids = old_and_new_id.split("@@@")
        global Server_Dict
        Server_Dict[old_and_new_ids[1]] = Server_Dict.pop(old_and_new_ids[0])

        self.to_ui_deposit_id()

    # 拿到处于连接状态的客户端，通过触发主流程绑定的信号，来向ui界面存入目标
    def to_ui_deposit_id(self):
        self.target_list = filtration_disconnect_flag_client()
        self.target_list.append("广播")
        self.signal_center.trigger_ComboBox_select_target(str(self.target_list))

    # 关闭全部客户端的runflag状态
    def closeThread(self):
        print("Server->closeThread->")
        for client in Server_Dict:
            Server_Dict[client].runFlag = False
        self.socket.close()


class Server_Thread(QThread):
    _flag = pyqtSignal(str)
    _send_info_c_to_c = pyqtSignal(str)
    _update_server_id = pyqtSignal(str)
    _send_info_all = pyqtSignal(str)

    def __init__(self, socket, server_id):
        super(Server_Thread, self).__init__()
        self.signal_center = Signal_Center()
        self.data_center = Data_Center()
        self.socket = socket
        self.server_id = server_id
        self.runFlag = True
        self.clientsocket = None
        self.target_list = []

    def run(self):
        print("Server_Thread->run->此线程ID{}".format(self.server_id))
        self.signal_center.trigger_StatusBar_signal("等待客户端连接。。。")
        self.clientsocket, self.addr = self.socket.accept()

        # 检测是否到达ui界面设置的最大连接数，
        # 未到达:将ip显示到UI、发送一个flag连接信号代表自身线程状态 连接状态则创建一个新线程等待连接
        # 到达：将自身状态置为断开状态 并将上一个新创建的待连接线程 从存储连接对象的全局变量Server_Dict 中清除
        global Server_Dict
        max_connect_number = self.data_center.get_connect_num()
        connect_number = len(Server_Dict)
        if connect_number <= int(max_connect_number):
            self.data_put_in_ui()
            self.sin_send_flag(0)
        else:
            self.send_to_client("服务端:服务端连接数量达到上限")
            self.sin_send_flag(1)
            if connect_number != int(max_connect_number):
                self.sin_send_flag(0)
            return

        # 自身线程变量runflag为Ture则循环接收消息
        self.receive_message()

    # 循环持续收消息
    def receive_message(self):
        print("Server_Thread->receive_message->")
        while self.runFlag:
            try:
                data = self.clientsocket.recv(1024).decode("utf-8")
                self.recv_message_select_whither(data)

            except Exception as reason:
                print("异常：Server_Thread->receive_message->{}".format(reason))
                self.sin_send_flag(1)
                data_join = "{}:结束连接".format(self.server_id)
                self.signal_center.trigger_Tedit_chat(data_join)
                self.sin_send_info_all(data_join)
                break

        self.clientsocket.close()
        self.signal_center.trigger_Tedit_chat("{}:线程关闭".format(self.server_id))

    # 判断循环接收到的消息，根据字符串第一个，判断如何执行
    def recv_message_select_whither(self, data):
        print("Server_Thread->recv_message_select_whither->{}".format(data))
        message = data.split("@@@")
        print("Server_Thread->recv_message_select_whither 根据@才分后的数据列表->{}".format(message))
        self.target_list = filtration_disconnect_flag_client()
        try:
            if message[0] == "服务端":
                data_join = "客户端名称：" + str(self.server_id) + " IP:" + str(self.addr) + "发送内容：" + message[1]
                self.signal_center.trigger_Tedit_chat(data_join)

                print("收消息判断处理 服务端：要发送出去的参数->{}".format(data_join))

            elif message[0] in self.target_list:
                data_join = "{}:发送内容为：@@@{}".format(self.server_id, str(data))
                self.sin_send_info_c_to_c(data_join)

                print("收消息判断处理 message[0] in self.target_list：要发送出去的参数-> {}".format(data_join))

            elif message[0] == "获取在线好友":
                target_list = ",".join(i for i in self.target_list)
                data_join = "@@@".join(["返回在线好友", target_list])
                self.signal_center.trigger_Tedit_chat(data_join)
                self.sin_send_info_all(data_join)

                print("收消息判断处理 获取在线好友：要发送出去的参数->{}".format(data_join))

            elif message[0] == "更新名称":
                data_join = "@@@".join([self.server_id, message[1]])
                self.sin_send_update_server_id(data_join)

                print("收消息判断处理 更新名称：要发送出去的参数->{}".format(data_join))

            else:
                data_join_host_name = "{}发送内容为:{}服务端只收未做其他处理".format(self.server_id, message[1])
                self.signal_center.trigger_Tedit_chat(data_join_host_name)

                print("收消息判断处理 未做处理：要发送出去的参数->{}".format(data_join_host_name))
        except Exception as reason:
            print("异常：Server_Thread->recv_message_select_whither->{}".format(reason))

    # 单个服务端线程内存储的实例对象具有的 自身发消息功能
    def send_to_client(self, text):
        print("Server_Thread->send_to_client->{}".format(text))
        try:
            self.clientsocket.send(text.encode("utf-8"))
        except Exception as reason:
            print("异常：Server_Thread->send_to_client->{}".format(reason))
            self.signal_center.trigger_Tedit_chat("{}结束连接".format(self.server_id))
            self.sin_send_flag(1)

    # 客户端连接成功时，存放目标与将ip与ID显示到聊天
    def data_put_in_ui(self):
        print("Server_Thread->data_put_in_ui->")
        text = "连接的客户端ip,port：{} ".format(self.addr)
        self.signal_center.trigger_Tedit_chat(text)

    # 服务端线程类声明的信号，服务端类已经将信号绑定到自身的槽函数上，通过触发服务端线程信号，就达到想要在服务端执行的操作
    def sin_send_flag(self, flag):
        print("Server_Thread->sin_send_flag->{}".format(flag))
        state_list = ["connect", "disconnect"]
        flags = "@@@".join([self.server_id, state_list[flag]])
        self._flag.emit(flags)

    def sin_send_info_all(self, data_join):
        print("Server_Thread->sin_send_info->{}".format(data_join))
        self._send_info_all.emit(data_join)

    def sin_send_info_c_to_c(self, data_join):
        print("Server_Thread->sin_send_info_c_to_c->{}".format(data_join))
        self._send_info_c_to_c.emit(data_join)

    def sin_send_update_server_id(self, data_join):
        print("Server_Thread->sin_send_update_server_id->{}".format(data_join))
        old_and_new_ids = data_join.split("@@@")
        self.server_id = old_and_new_ids[1]
        self._update_server_id.emit(data_join)
