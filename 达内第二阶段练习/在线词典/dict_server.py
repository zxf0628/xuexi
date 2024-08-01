import time
from socket import *
from threading import *
import sys, os
import dict_db

# log_path = './applog.log'
# if os.path.exists(log_path):
#     os.remove(log_path)

import logging.config


logging.config.fileConfig("../log_package/logginga.conf")
logger = logging.getLogger()

# 全局变量
HOST = "127.0.0.1"
PORT = 8886
ADDR = (HOST, PORT)
DB = dict_db.Entrance()


# 处理线程类
class Handle_Thread(Thread):
    def __init__(self, c):
        super(Handle_Thread, self).__init__()
        self.client_obj = c
        self.cur = DB.create_cursor()
        self.state = True

    def run(self):
        while self.state:
            info = self.client_obj.recv(1024)
            self.judge_agreement(info.decode())

        DB.close_cursor()
        self.client_obj.close()

    def judge_agreement(self, agreement):
        agreement = agreement.split()
        if agreement:
            logger.debug("Handle_Thread---judge_agreement---%s" % agreement)
        if not agreement or agreement == "E":
            self.state = False
        elif agreement[0] == "R":
            self.register(agreement[1],agreement[2])
        elif agreement[0] == "L":
            self.login(agreement[1],agreement[2])
        elif agreement[0] == "S":
            self.select_word(agreement[1],agreement[2])
        elif agreement[0] == "H":
            self.select_hist(agreement[1])

    def register(self,name,password):
        logger.debug("Handle_Thread---register---%s %s" % (name,password))
        if DB.register(name,password):
            self.send_data("OK")
        else:
            self.send_data('用户名以存在')

    def login(self,name,password):
        logger.debug("Handle_Thread---login---%s    %s" % (name, password))
        if DB.login(name, password):
            self.send_data("OK")
        else:
            self.send_data('登录失败,用户名或密码错误')

    def select_word(self,name,word):
        DB.insert_hist(name,word)

        logger.debug("Handle_Thread---select_word---%s    %s" % (name,word))
        result = DB.select_word(name,word)
        logger.debug("Handle_Thread---select_word---查询结果：%s" % result)
        if result:
            self.send_data(result)
        else:
            self.send_data('无此单词')

    def select_hist(self,name):
        logger.debug("Handle_Thread---select_hist---%s " % name)
        result = DB.select_hist(name)
        if result:
            self.send_data('OK')
        else:
            self.send_data('无此单词')

        for i in result:
            msg = '%s   %-16s   %s' % i
            time.sleep(0.1)
            self.send_data(msg)
        time.sleep(0.1)
        self.send_data('##')

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
        logger.debug("main---等待连接。。。")
        c, c_addr = s.accept()
        logger.debug("main---客户端：%s 连接成功" % str(c_addr))
        try:
            t = Handle_Thread(c)
            t.daemon = True
            t.start()

        except KeyboardInterrupt:
            s.close()
            DB.close()
            sys.exit()

        except Exception as e:
            logger.debug("main---主循环异常：%s" % str(e))
            continue


if __name__ == "__main__":
    main()
