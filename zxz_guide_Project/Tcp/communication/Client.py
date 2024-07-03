import socket
from PyQt5.QtCore import *


class Client():  # 主机默认为本地主机,
    def __init__(self, widget, ip, hostName, port):
        self.widget = widget
        self.ip = ip
        self.host = hostName  # 获得该主机名
        self.port = port  # 设定默认端口号(服务器端口号和客户端接入端口号都是这个默认端口)

        self.target = widget.select_target

        self.buildSocket()


    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buildClient()

    def buildClient(self):
        self.client = ClientThread(self.socket,self.target)  # 获取连接

        self.client._flag.connect(self.getFlag)
        self.client._signal.connect(self.getMessage)
        self.client._text.connect(self.getText)
        if self.client.connectServer(self.ip, self.port):
            self.client.start()
            print("connected prot = " + str(self.port))
        else:
            print("cannt connected prot = " + str(self.port))

    # 发送消息
    def sendToServer(self, text):  # 向服务器发送消息
        target_content = self.target.currentText()
        text_full = "@@@".join([target_content,text])
        try:
            self.socket.send(text_full.encode('utf-8'))
        except Exception as reason:
            self.getMessage(reason)
            self.getFlag("disconnect")  # 发送连接失败标志

    def btnsend(self, text):
        self.sendToServer(text)

    def closeThread(self):
        self.runflag = False

    def getFlag(self, flag):
        if flag == "connect":
            self.widget.statusBar.showMessage("连接成功！！！")
        elif flag == "disconnect":
            self.client.runflag = False
        else:
            self.client.runflag = False

    def getMessage(self, signal):
        self.widget.statusBar.showMessage(signal)

    def getText(self, text):
        self.widget.Tedit_chat.append(text)

    def btnsend_c_to_c(self,text_full):
        try:
            self.socket.send(text_full.encode('utf-8'))
        except Exception as reason:
            self.getMessage(reason)
            self.getFlag("disconnect")  # 发送连接失败标志



class ClientThread(QThread):
    _signal = pyqtSignal(str)
    _text = pyqtSignal(str)
    _flag = pyqtSignal(str)

    def __init__(self, serverSocket,target):
        super(ClientThread, self).__init__()
        self.serverSocket = serverSocket
        self.runflag = True
        self.connectList = ["connect", "disconnect"]  # 连接成功与连接失败

        self.target = target

    def connectServer(self, ip, port):
        try:
            self.serverSocket.connect((ip, port))
            self.sendFlag(0)  # 发送连接成功标志
            return True
        except Exception as reason:
            self.sendMessage(reason)
            self.sendFlag(1)  # 发送链接失败标志
            return reason

    def run(self):
        while self.runflag:
            try:
                # 接受服务端消息
                msg = self.serverSocket.recv(1024).decode("utf-8")

                self.recv_msg_by_type(msg)

                # self.sendText(msg)
            except Exception as reason:
                self.sendMessage(reason)
                self.sendFlag(1)  # 发送连接失败标志
                break

    def sendMessage(self, message):
        self._signal.emit(str(message))

    def sendText(self, text):
        self._text.emit(str(text))

    def sendFlag(self, flagIndex):
        self._flag.emit(str(self.connectList[flagIndex]))

    def recv_msg_by_type(self,msg):
        text_full = msg.split("@@@")
        filter_target_lists = [self.target.itemText(i) for i in range(self.target.count())]
        if text_full[0] == "返回在线好友":
            target_lists = text_full[1].split(",")
            target_lists.append("服务端")
            print(target_lists)
            target_lists = list(set(target_lists) - set(filter_target_lists))
            self.target.addItems(target_lists)
            self.sendText(text_full)
        else:
            self.sendText(msg)
