"""
主程序
实现流程：
    创建一个接受浏览器的服务端，每有一个连接创建一个线程对象来处理
    通过正则表达式 提取出访问类型及页面地址信息
    将此信息通过json格式 传输给另一个后端逻辑处理的服务端 后端服务器在反馈给状态码和数据
    将后端反馈的数据在通过符合浏览器接收的格式 发送回去

"""

from socket import *
import threading
import config
import re
import json
import logging.config

# logging.config.fileConfig("../log_package/logginga.conf")
logging.config.fileConfig("E:\A_python_project\Project_Exercise\达内第二阶段练习\log_package\logginga.conf")
logger = logging.getLogger()


def connect_frame(env):
    logger.debug("---connect_frame---%s" % str(env))
    s = socket()
    # 连接失败返回空
    try:
        s.connect((config.frame_ip, config.frame_port))
    except:
        return

    data = json.dumps(env).encode()
    s.send(data)

    # 收数据frame服务端异常返回空
    try:
        data = s.recv(1024 * 1024 * 10).decode()  # {status:200,data:数据}
        logger.debug("---connect_frame-return-%s" % str(json.loads(data)))
        return json.loads(data)
    except:
        return


class HttpServer:
    def __init__(self):
        self.HOST = config.HOST
        self.PROT = config.PORT
        self.ADDR = (self.HOST, self.PROT)

        self.create_socket()
        self.bing_socket()

    def create_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, config.Debug)

    def bing_socket(self):
        self.s.bind(self.ADDR)
        self.s.listen(5)

    def server_forever(self):
        while True:
            logger.debug("HttpServer---server_forever---开始主循环 接收服务器访问")
            connfd, addr = self.s.accept()

            logger.debug("HttpServer---server_forever---连接成功：%s" % str(addr))

            t = threading.Thread(target=self.handle, args=(connfd,))
            t.daemon = True
            t.start()

    def handle(self, connfd):
        request = connfd.recv(6666).decode()

        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'

        try:
            env = re.match(pattern, request).groupdict()  # {method:GET,info:./}
            logger.debug("HttpServer---handle---访问内容：%s" % str(env))
        except:
            connfd.close()
            return
        else:
            data = connect_frame(env)
            if data:
                logger.debug("HttpServer---handle---webframe处理后返回数据：%s" % str(data))
                self.response(connfd, data)

    def response(self, connfd, data):
        logger.debug("HttpServer---response---%s  " % str(data['status']))
        logger.debug("HttpServer---response---%s  " % str(data['data']))
        if data['status'] == 200:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            responseBody = data['data']
        elif data['status'] == 404:
            response = "HTTP/1.1 404 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            responseBody = data['data']
        else:
            response = "HTTP/1.1 404 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            responseBody = 'not_200 and not_404'
        response_data = response + responseBody
        logger.debug("HttpServer---response---回发给http数据：%s" % str(response_data))
        connfd.send(response_data.encode())


if __name__ == '__main__':
    https = HttpServer()
    https.server_forever()