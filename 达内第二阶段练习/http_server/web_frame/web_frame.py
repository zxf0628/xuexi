import json
from socket import *
from threading import *
import sys, os
import logging.config
import settings
from urls import *

# logging.config.fileConfig("../log_package/logginga.conf")
logging.config.fileConfig("E:\A_python_project\Project_Exercise\达内第二阶段练习\log_package\logginga.conf")
logger = logging.getLogger()


# 处理线程类
class Application(Thread):
    def __init__(self, c):
        super(Application, self).__init__()
        self.client_obj = c

    def run(self):
        requset = self.client_obj.recv(1024).decode()
        requset = json.loads(requset)
        logger.debug("Application---run---收到webserver：%s" % str(requset))
        if requset["info"] == "/favicon.ico":
            logger.debug("Application---run---有是你favicon.ico滚！")
            return
        if requset['method'] == 'GET':
            if requset["info"] == "/" or requset["info"][-5:] == ".html":
                response = self.get_html(requset["info"])
            else:
                response = self.get_data(requset["info"])
        response_data = json.dumps(response)
        logger.debug("Application---run---回发webserver：%s" % str(response_data))
        self.send_data(response_data)
        self.client_obj.close()

    def get_html(self, info):
        logger.debug("Application---get_html---%s" % str(info))
        static = settings.STATIC_PATH
        if info == "/":
            filename = static + "/index.html"
        else:
            filename = static + info

        logger.debug("Application---get_html---打开文件路径:%s" % str(filename))

        try:
            f = open(filename, "r", encoding='utf-8')
        except:
            with open(static + "/404.html") as fd:
                data = {'status': 404, 'data': fd.read()}
                logger.debug("Application---get_html---打开文件失败 404:%s" % str(data))
                return data
        else:
            data = {'status': 200, 'data': f.read()}
            logger.debug("Application---get_html---打开文件成功 200:%s" % str(data))
            return data

    def get_data(self, info):
        logger.debug("Application---get_data---%s" % str(info))
        for url, func in urls:
            logger.debug("Application---get_data---查看数据处理路由是否支持:%s" % str(url))
            if url == info:
                logger.debug("Application---get_data---数据处理路由支持 要执行:%s" % str(url))
                return {'status': 200, 'data': func()}
        return {'status': 404, 'data': '没有实现当前的获取数据处理函数'}


    def send_data(self, data):
        # logger.debug("Handle_Thread---send_data---%s" % data)
        self.client_obj.send(data.encode())


# 搭建网络模型
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, settings.Debug)
    s.bind((settings.frame_ip, settings.frame_port))
    s.listen()

    while True:
        logger.debug("等待webserver连接。。。")
        c, c_addr = s.accept()
        logger.debug("webserver客户端：%s 连接成功" % str(c_addr))
        try:
            t = Application(c)
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
