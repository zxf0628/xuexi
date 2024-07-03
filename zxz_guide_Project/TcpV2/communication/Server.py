import socket

from PyQt5.QtCore import QThread
from TcpV2.data_centers.data_transfer import Data_Center
from TcpV2.signal_centers.signal_transfer import Signal_Center

Server_Dict = {}
Server_id = 1


class Server():
    def __init__(self):
        self.data_center = Data_Center()
        self.signal_center = Signal_Center()
        self.target_connect = None
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

        self.signal_center._flag.connect(self.sin_get_flag)
        self.signal_center._send_info.connect(self.send_info_to_all)
        self.signal_center._send_info_c_to_c.connect(self.btnsend_c_to_c)
        self.signal_center._update_server_id.connect(self.sin_update_server_id)
        server.start()

    # 发送消息
    def send_info(self, text):
        print("Server->send_info->{}".format(text))
        self.target_connect = self.data_center.get_select_target()
        if self.target_connect == "广播" or self.target_connect == "":
            self.send_info_to_all(text)
        else:
            self.send_info_to_target(text)


    def send_info_to_all(self, text):
        print("Server->send_info_to_all->{}".format(text))
        for client in Server_Dict:
            try:
                if Server_Dict[client].clientsocket is not None:
                    Server_Dict[client].send_to_client(text)
                    print("Server->send_info_to_all 完成发送->{}".format(text))
            except Exception as reason:
                self.signal_center.trigger_flag("@@@".join([client, "disconnect"]))
                self.signal_center.trigger_StatusBar_signal("服务端向客户端广播消息失败")
                print("异常：Server->send_info_to_all->{}".format(reason))

    def send_info_to_target(self, text):
        print("Server->send_info_to_target->{}".format(text))
        try:
            if Server_Dict[self.target_connect].clientsocket is not None:
                Server_Dict[self.target_connect].send_to_client(text)
        except Exception as reason:
            self.signal_center.trigger_flag("@@@".join([self.target_connect, "disconnect"]))
            self.signal_center.trigger_StatusBar_signal("服务端向客户端发送消息失败")
            print("异常：Server->send_info_to_target->{}".format(reason))

    # ui界面点击发送按钮，触发的发送功能，与信号text功能一致
    def btnsend(self, text):
        print("Server->btnsend->{}".format(text))
        self.signal_center.trigger_Tedit_chat(text)
        self.send_info(text)

    def btnsend_c_to_c(self,text):
        print("Server->btnsend_c_to_c->{}".format(text))
        datas = text.split("@@@")
        data_join = " ".join([datas[0], datas[2]])
        try:
            if Server_Dict[datas[1]].clientsocket != None:
                Server_Dict[datas[1]].sendToClient(data_join)
        except Exception as reason:
            print("异常：Server->btnsend_c_to_c->{}".format(reason))

    # 根据触发的信号来管理，全局变量下客户端的runflag状态
    def sin_get_flag(self, flag):
        print("Server->sin_get_flag->{}".format(flag))
        flags = flag.split("@@@")
        if flags[1] == "connect":
            '''占位  一个判断全局变量存储客户端个数的字典 是否符合ui设置最大连接数'''
            self.buildServer()
        elif flags[1] == "disconnect":
            global Server_Dict
            Server_Dict[flags[0]].runFlag = False
            print("Server->sin_get_flag->修改线程状态后 全局变量Server_Dict：{}".format(Server_Dict[flags[0]].runFlag))
            # del Server_Dict[flags[0]]
            print("Server->sin_get_flag->修改线程状态并清除后 全局变量Server_Dict：{}".format(Server_Dict))

    def sin_update_server_id(self,old_and_new_id):
        print("Server->sin_update_server_id->{}".format(old_and_new_id))
        old_and_new_ids = old_and_new_id.split("@@@")
        global Server_Dict
        global Server_id
        Server_Dict[old_and_new_ids[1]] = Server_Dict.pop(old_and_new_ids[0])

        self.target_list = [str(i) for i in Server_Dict.keys()]
        self.signal_center.trigger_ComboBox_select_target(str(self.target_list))

    # 关闭全部客户端的runflag状态
    def closeThread(self):
        print("Server->closeThread->")
        for client in Server_Dict:
            Server_Dict[client].runFlag = False


class Server_Thread(QThread):
    def __init__(self, socket, server_id):
        super(Server_Thread, self).__init__()
        self.socket = socket
        self.server_id = server_id
        self.runFlag = True
        self.clientsocket = None
        self.signal_center = Signal_Center()

    def run(self):
        print("Server_Thread->run->此线程ID{}".format(self.server_id))
        self.signal_center.trigger_StatusBar_signal("等待客户端连接。。。")
        self.clientsocket, self.addr = self.socket.accept()

        # 通过信号向主界面存目标
        self.target_list = [str(i) for i in Server_Dict.keys()]
        self.signal_center.trigger_ComboBox_select_target(str(self.target_list))

        text = "连接的客户端ip：{} 客户端名称：{}".format(self.addr, self.server_id)
        self.signal_center.trigger_Tedit_chat(text)
        
        self.send_flag(0)
        self.receive_message()

    # 服务端类定义的信号，服务端线程类 触发
    def send_flag(self, flag):
        print("Server_Thread->send_flag->{}".format(flag))
        state_list = ["connect", "disconnect"]
        flags = "@@@".join([self.server_id,state_list[flag]])
        self.signal_center.trigger_flag(flags)

    # 循环持续收消息
    def receive_message(self):
        print("Server_Thread->receive_message->")
        while self.runFlag:
            try:
                data = self.clientsocket.recv(1024).decode("gbk")
                self.recv_message_select_whither(data)

            except Exception as reason:
                print("异常：Server_Thread->receive_message->{}".format(reason))
                self.send_flag(1)
                # self.signal_center.trigger_StatusBar_signal("服务端线程持续接收函数异常:"+str(reason))
                text = "{}:结束连接".format(self.server_id)
                self.signal_center.trigger_Tedit_chat(text)
                self.signal_center.trigger_send_info(text)
                self.clientsocket.close()
                break

        # self.clientsocket.close()
        # self.signal_center.trigger_Tedit_chat("{}:线程关闭".format(str(self.server_id)))

    # 判断循环接收到的消息，根据字符串第一个，判断如何执行
    def recv_message_select_whither(self, data):
        print("Server_Thread->recv_message_select_whither->{}".format(data))
        message = data.split("@@@")
        print("Server_Thread->recv_message_select_whither 根据@才分后的数据列表->{}".format(message))
        if message[0] == "服务端":
            data_join = str(self.addr) + "发送内容为：" + message[1]
            self.signal_center.trigger_Tedit_chat(data_join)

            print("收消息判断处理 服务端：要发送出去的参数->{}".format(data_join))

        elif message[0] in self.target_list:
            data_join = "{}:发送内容为：@@@：{}".format(self.server_id, str(data))
            self.signal_center.trigger_send_info_c_to_c(data_join)

            print("收消息判断处理 message[0] in self.target_list：要发送出去的参数->{}".format(data_join))

        elif message[0] == "获取在线好友":
            target_list = ",".join(str(i) for i in self.target_list)
            data_join = "@@@".join(["返回在线好友", target_list])
            self.signal_center.trigger_Tedit_chat(data_join)
            self.signal_center.trigger_send_info(data_join)

            print("收消息判断处理 获取在线好友：要发送出去的参数->{}".format(data_join))

        elif message[0] == "更新名称":
            data_join = "@@@".join([self.server_id,message[1]])
            self.signal_center.trigger_update_server_id(data_join)

            print("收消息判断处理 更新名称：要发送出去的参数->{}".format(data_join))

        else:
            data_join_host_name = "{}发送内容为:{}服务端只收未做其他处理".format(self.server_id,message[1])
            self.signal_center.trigger_StatusBar_signal(data_join_host_name)

            print("收消息判断处理 未做处理：要发送出去的参数->{}".format(data_join_host_name))

    # 单个服务端线程内存储的实例对象具有的 自身发消息功能
    def send_to_client(self, text):
        print("Server_Thread->send_to_client->{}".format(text))
        try:
            self.clientsocket.send(text.encode("utf-8"))
        except Exception as reason:
            print("异常：Server_Thread->send_to_client->{}".format(reason))
            self.signal_center.trigger_StatusBar_signal("{}结束连接".format(self.server_id))
            self.send_flag(1)
