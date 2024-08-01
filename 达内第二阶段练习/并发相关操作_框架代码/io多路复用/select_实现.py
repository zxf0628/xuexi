import sys
from select import select
from socket import *
from time import ctime

rlist = []
wlist = []
xlist = []

ADDR = ("127.0.0.1", 8886)
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)
s.bind(ADDR)
s.listen()
s.setblocking(False)

rlist.append(s)
# rlist.append(sys.stdin)

f_log = open("log.txt", "a")

while True:
    rs, ws, xs = select(rlist, wlist, xlist)

    for r in rs:
        if r is s:
            c, addr = r.accept()
            f_log.write("%s  %s" % (ctime(), addr))
            f_log.flush()
            c.setblocking(False)
            rlist.append(c)
        elif r is sys.stdin:
            f_log.write("%s  %s"%(ctime(),r.readline()))
            f_log.flush()
        else:  # c
            data = r.recv(1024).decode()
            if not data:
                rlist.remove(r)
                r.close()
                continue
            f_log.write("%s  %s" % (ctime(), data))
            f_log.flush()

    # for w in ws:
    #     w.send(b"OK")

