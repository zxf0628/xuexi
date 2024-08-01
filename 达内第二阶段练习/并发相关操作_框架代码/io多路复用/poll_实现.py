import select
import sys
from select import *
from socket import *
from time import ctime


ADDR = ("127.0.0.1", 8886)
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)
s.bind(ADDR)
s.listen()
s.setblocking(False)

f_log = open("log.txt", "a")

p = poll()
p.register(s,POLLIN)

fdmap = {s.fileno():s}

while True:
    events = p.poll()

    for fd,event in events:
        if fd == s.fileno():
            c,addr = fdmap[fd].accept()
            c.setblocking(False)
            fdmap[c.fileno()] = c

        elif event & POLLIN: # 通过监听返回的操作标识符 判断是否为收消息
            data = fdmap[fd].recv(1024)
            if not data:
                p.unregister(fdmap[fd])
                fdmap[fd].close()
                del(fdmap[fd])
                continue
            f_log.write("%s  %s" % (ctime(), data))
            f_log.flush()

