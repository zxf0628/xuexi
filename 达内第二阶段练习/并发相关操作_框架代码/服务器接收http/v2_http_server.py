from socket import *
from select import *


class HTTPServer:
    def __init__(self,ADDR,DIR):
        self.addr = ADDR
        self.dir = DIR

        self.rlist = []
        self.wlist = []
        self.xlist = []

        self.initialize_socket()
        self.bind()

    def initialize_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)
        self.s.setblocking(False)

    def bind(self):
        self.s.bind(self.addr)

    def serverforever(self):
        self.s.listen(5)
        self.rlist.append(self.s)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)

            for r in rs:
                if r is self.s:
                    c, addr = r.accept()
                    c.setblocking(False)
                    self.rlist.append(c)
                else:
                    self.handle(r)

    def handle(self,c_socket_obj):
        data = c_socket_obj.recv(4646)
        if not data:
            self.rlist.remove(c_socket_obj)
            c_socket_obj.close()
            return

        request_line = data.decode().split("\n")[0]
        info = request_line.split(" ")[1]

        if info == "/" or info[-5:] == ".html":
            self.get_html(c_socket_obj,info)
        else:
            self.get_data(c_socket_obj,info)

    def get_html(self,c_socket_obj,info):
        if info == "/":
            filename = self.dir + "/index.html"
        else:
            filename = self.dir + info
        try:
            f = open(filename,"r",encoding='utf-8')
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry not html.....</h1>"
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += f.read()
        c_socket_obj.send(response.encode())

    def get_data(self,c_socket_obj,info):
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "还没开发写完呢:"+info
        c_socket_obj.send(response.encode())


if __name__ == "__main__":
    ADDR = ("127.0.0.1",8888)
    DIR = "./html文件"
    http = HTTPServer(ADDR,DIR)
    http.serverforever()