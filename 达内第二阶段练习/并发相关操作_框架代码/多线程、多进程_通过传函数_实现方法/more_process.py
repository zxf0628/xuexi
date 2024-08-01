import socket
import threading
import multiprocessing


ADDR = ("127.0.0.1",8888)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
s.bind(ADDR)
s.listen()


def handle(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print("c:",data.decode())
        c.send(b"OK")
    c.close()


# 循环等待客户端连接
while True:
    c,addr = s.accept()
    print("Connect from:",addr)

    # p = multiprocessing.process(target=handle,args=(c,))
    t = threading.Thread(target=handle,args=(c,))
    t.daemon = True
    t.start()