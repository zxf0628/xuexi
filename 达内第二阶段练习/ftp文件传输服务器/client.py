import sys
import time
from socket import *
import logging.config

logging.config.fileConfig("../log_package/logginga.conf")
logger = logging.getLogger()

# 全局变量
HOST = "127.0.0.1"
PORT = 8886
ADDR = (HOST, PORT)


class Client():
    def __init__(self):
        self.s = socket()
        self.connect()

    def connect(self):
        try:
            self.s.connect(ADDR)
            logger.debug("Client---connect--- ---连接服务器成功")
        except Exception as e:
            print(e)
            return

    def main(self):
        while True:
            logger.debug("Client---main--- ---循环向服务器发送请求")
            agreement = input("\n L(查看本地文件),P(上传文件),G(获取文件),Q(退出) 请输入命令：")
            self.judge_agreement(agreement)

    def judge_agreement(self,agreement):
        logger.debug("Client---judge_agreement---%s" % agreement)
        if agreement == "L":
            self.Local()

        elif agreement[:1] == "P":
            filename = agreement.split(" ")[-1]
            self.Put(filename)

        elif agreement[:1] == "G":
            filename = agreement.split(" ")[-1]
            self.Get(filename)

        elif agreement == "Q":
            self.send_info("Q")
            self.s.close()
            sys.exit("谢谢使用")

        else:
            print("请输入正确命令")
            return

    def send_info(self,info):
        logger.debug("Client---send_info---%s" % info)
        self.s.send(info.encode())

    def recv_info(self):
        data = self.s.recv(1024 * 1024).decode()
        logger.debug("Client---recv_info---%s" % data)
        return data

    def Local(self):
        logger.debug("Client---Local---" )
        self.send_info("L")
        data = self.recv_info()
        if data == "OK":
            data = self.recv_info()
            print(data)
        else:
            print(data)

    def Get(self,filename):
        logger.debug("Client---Get---")
        self.send_info("G "+filename)
        data = self.recv_info()
        if data == "OK":
            f = open(filename,"wb")
            while True:
                f_data = self.recv_info()
                if f_data == "##":
                    break
                f.write(f_data.encode())
            f.close()
        else:
            print(data)

    def Put(self,filename):
        try:
            f = open(filename,"rb")
        except Exception as e:
            logger.debug("Client---judge_agreement--- ---无法提交文件:%s" % e)
            print("Client---judge_agreement--- ---无法提交文件:%s" % e)
            return

        self.send_info("P "+filename)
        data = self.recv_info()
        if data == "OK":
            while True:
                file_data = f.read(1024)
                if not file_data:
                    time.sleep(0.1)
                    self.send_info("##")
                    break
                self.send_info(file_data.decode())
            f.close()
        else:
            print(data)


if __name__ == "__main__":
    c = Client()
    c.main()
