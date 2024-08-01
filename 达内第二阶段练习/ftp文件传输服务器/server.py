import time
from socket import *
from threading import *
import sys, os
import logging.config

logging.config.fileConfig("../log_package/logginga.conf")
logger = logging.getLogger()

# 全局变量
HOST = "127.0.0.1"
PORT = 8886
ADDR = (HOST, PORT)
FTP_PATH = "./ftp文件库/"


# 处理线程类
class Handle_Thread(Thread):
    def __init__(self, c):
        super(Handle_Thread, self).__init__()
        self.client_obj = c

    def run(self):
        while True:
            info = self.client_obj.recv(1024)
            self.judge_agreement(info.decode())

    def judge_agreement(self, agreement):
        if agreement:
            logger.debug("Handle_Thread---judge_agreement---%s" % agreement)
        if not agreement or agreement == "Q":
            return

        elif agreement == "L":
            self.Local()

        elif agreement[:1] == "P":
            filename = agreement.split(" ")[-1]
            self.Put(filename)

        elif agreement[:1] == "G":
            filename = agreement.split(" ")[-1]
            self.Get(filename)

    def Local(self):
        logger.debug("Handle_Thread---Local---")
        local_files = os.listdir(FTP_PATH)
        logger.debug("文件库文件列表：%s" % local_files)

        if not local_files:
            self.send_data("文件库为空")
            return
        else:
            self.send_data("OK")
            time.sleep(0.1)

        local_files = "\n".join(local_files)
        self.send_data(local_files)

    def Put(self, filename):
        if os.path.exists(FTP_PATH + filename):
            self.send_data("无法上传 本地文件库存在此文件")
            return
        else:
            self.send_data("OK")
        f = open(FTP_PATH + filename, "wb")
        while True:
            file_data = self.client_obj.recv(1024)
            if file_data == b"##":
                break
            f.write(file_data)
        f.close()

    def Get(self, filename):
        try:
            f = open(FTP_PATH + filename, "rb")
        except Exception as e:
            self.send_data("文件库不存在此文件")
        else:
            self.send_data("OK")

        while True:
            file_data = f.read(1024)
            if not file_data:
                self.send_data("##")
                break
            self.send_data(file_data.decode())
        f.close()

    def send_data(self, data):
        logger.debug("Handle_Thread---send_data---%s" % data)
        self.client_obj.send(data.encode())


# 搭建网络模型
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    s.bind(ADDR)
    s.listen()

    while True:
        logger.debug("等待连接。。。")
        c, c_addr = s.accept()
        logger.debug("客户端：%s 连接成功" % str(c_addr))
        try:
            t = Handle_Thread(c)
            t.daemon = True
            t.start()

        except KeyboardInterrupt:
            s.close()
            sys.exit()
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
