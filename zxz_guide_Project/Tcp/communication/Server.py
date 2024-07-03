import socket
from PyQt5.QtCore import *


class Server:
    def __init__(self, widget, ip, host, port):
        self.widget = widget
        self.ip = ip
        self.host = host
        self.port = port
        self.target = widget.select_target

        self.server_Dict = {}
        self.server_Id = 0

        self.buildSocket()

    # 建立套接字
    def buildSocket(self):
        client_num = self.widget.Ledit_client_num.text()
        if client_num == "": client_num = 5
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(client_num)

        self.buildServer()

    # 建立服务器
    def buildServer(self):
        server = Server_Thread(self.socket, str(self.server_Id), self.target, self.server_Dict)
        # 存入的是一整个 子线程实列对象 也是 客户端实例对象
        self.server_Dict[str(self.server_Id)] = server
        self.server_Id += 1

        # 绑定信号与槽函数   信号被触发  运行绑定的函数
        server._flag.connect(self.getFlag)
        server._text.connect(self.getText)
        server._singal.connect(self.getMessage)
        server._text_c.connect(self.get_bordCastInfo_client_to_client)

        server.start()

    # getText触发   向服务端实例对象下 指定客户端套接字 发送消息
    def bordCastInfo(self, text):
        self.target_connet = self.target.currentText()
        try:
            if self.target_connet == "广播" or self.target_connet == "":
                print("返回好友信息：")
                print(text)
                self.bordCastInfo_to_all(text)
            else:
                self.bordCastInfo_to_target(text)
        except:
            pass

    def bordCastInfo_to_all(self, text):
        for client in self.server_Dict:
            try:
                # 遍历拿到了每个服务器实例对象,判断服务器对象是否有客户端连接
                if self.server_Dict[client].clientsocket != None:
                    print(self.server_Dict[client])
                    # 将消息传入指定的客户端  就是这个服务器实例对象调用  客户端套接字发送函数
                    self.server_Dict[client].sendToClient(text)
            except Exception as reason:
                self.getFlag("@@@".join([client, "disconnect"]))
                print("服务端", reason)

    def bordCastInfo_to_target(self, text):
        try:
            if self.server_Dict[self.target_connet].clientsocket != None:
                self.server_Dict[self.target_connet].sendToClient(text)
        except Exception as reason:
            self.getFlag("@@@".join([self.target_connet, "disconnect"]))

    def get_bordCastInfo_client_to_client(self, data_full):
        text = data_full.split("@@@")
        data = " ".join([text[0], text[2]])
        try:
            if self.server_Dict[text[1]].clientsocket != None:
                self.server_Dict[text[1]].sendToClient(data)
        except Exception as reason:
            self.getFlag("@@@".join([self.target_connet, "disconnect"]))

    # 自定义信号触发   将消息写入控件聊天框 并 发送消息
    def getText(self, text):
        self.widget.Tedit_chat.append(text)
        self.bordCastInfo(text)

    # 自定义信号触发  将服务器实例对象 状态修改
    def getFlag(self, flag):
        flag = flag.split("@@@")
        if flag[1] == "connect":
            if self.server_Id <= 5:
                self.buildServer()
            else:
                self.widget.statusBar.showMessage("连接数量以上线")
        elif flag[1] == "disconnect":
            self.server_Dict[flag[0]].runflag = False

    # 自定义信号触发  将服务器实例对象对应错误信息  发送到控件状态栏中
    def getMessage(self, signal):
        signal = signal.split("@@@")
        self.widget.statusBar.showMessage("服务器Id:" + signal[0] + "状态：" + signal[1])

    # 发送控件触发  将消息写入控件聊天框 并 发送消息
    def btnsend(self, text):
        self.widget.Tedit_chat.append(text)
        self.bordCastInfo(text)

    # 关闭所有服务
    def closeThread(self):
        for i in self.server_Dict:
            self.server_Dict[i].runflag = False


class Server_Thread(QThread):
    # 声明信号
    _singal = pyqtSignal(str)
    _text = pyqtSignal(str)
    _flag = pyqtSignal(str)
    _text_c = pyqtSignal(str)

    def __init__(self, server_socket, server_Id, select_target, server_Dict):
        super(Server_Thread, self).__init__()
        self.server_Id = server_Id
        self.socket = server_socket
        self.target = select_target
        self.server_Dict = server_Dict
        self.client = []

        self.clientsocket = None  # 初始客户端套接字 初始未有用户连接
        self.addr = None  # 初始客户端IP与端口
        self.runflag = True  # 客户端套接字连接状态
        self.connectList = ["connect", "disconnect"]  # 赋予客户端套接字状态  连接与断开

    def run(self):
        self.send_Message("等待客户端连接。。。")
        self.clientsocket, self.addr = self.socket.accept()
        self.store_target()

        self.send_text("连接的客户端ip：{} 目标号：{}".format(self.addr, self.server_Id))
        # 这里此时有创建了一个新的 子线程服务端  等待客户端连接
        self.send_flag(0)
        self.get_Message()

    # 存入客户端目标,目标字典中存入的键值对与服务器的键值对没有关联，只是Id一样
    def store_target(self):
        self.target_list = [str(i) for i in self.server_Dict.keys()]
        filter_target_lists = [self.target.itemText(i) for i in range(self.target.count())]
        self.target_list.append("广播")
        target_list = list(set(self.target_list) - set(filter_target_lists))
        self.target.addItems(target_list)

    # 触发自定义_text信号 消息添加到聊天框并发送消息
    def send_text(self, text):
        self._text.emit(text)
        print(text)

    # 触发自定义_flag信号 修改实例对象连接状态
    def send_flag(self, flag):
        # 用 @@@.join  将列表的内容 进行拼接
        self._flag.emit("@@@".join([self.server_Id, self.connectList[flag]]))

    # 触发自定义_singal信号 将提示消息发送至状态框
    def send_Message(self, Message):
        self._singal.emit("@@@".join([self.server_Id, Message]))

    # 持续接受消息    收
    def get_Message(self):
        while self.runflag:
            try:
                data_full = self.clientsocket.recv(1024).decode("utf-8")
                print(data_full)

                self.recv_msg_by_type(data_full)

            except Exception as reason:
                self.send_Message(str(reason))
                self.send_text(str(self.addr) + "结束连接")
                self.send_flag(1)
                break
        self.clientsocket.close()
        self.send_text(self.server_Id + "线程关闭")

    # 对当前服务器实例对象中客户端套接字 进行消息发送      发
    def sendToClient(self, text):
        try:
            self.clientsocket.send(text.encode("utf-8"))
            print("发送成功，消息内容为:{}".format(text))
        except Exception as reason:
            print("消息发送失败原因：" + str(reason))
            self.send_Message(str(self.addr) + "结束连接")
            self.send_flag(1)

    # 判断接收到的消息，目的是干什么
    def recv_msg_by_type(self, data_full):
        friend_list = [str(i) for i in self.server_Dict.keys()]
        del (friend_list[-1])
        message = data_full.split("@@@")

        # 发给服务端 服务端广播给各个客户端
        if message[0] == "服务端":
            data = str(self.addr) + "发送内容为：" + message[1]
            self.send_text(data)
            print("接收成功")
        elif message[0] in friend_list:
            data_full = str(self.addr) + "发送内容为：@@@" + str(data_full)
            self._text_c.emit(data_full)
        elif message[0] == "获取在线好友":
            target_lists = ",".join(str(i) for i in friend_list)
            self.send_text("@@@".join(["返回在线好友", target_lists]))
        else:
            self.send_Message("目标选项错误")
            print(data_full)
