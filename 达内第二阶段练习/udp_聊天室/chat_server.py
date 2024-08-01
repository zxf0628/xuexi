import socket


USER = {}
ADDR = ("127.0.0.1", 8888)


def do_request(sk):
    while True:
        data, client_addr = sk.recvfrom(1024)
        command = data.decode().split("@@@")
        if command[0] == "L":
            do_login(sk,command[1],client_addr)


def do_login(sk,name,client_addr):
    global USER
    if name in USER:
        sk.sendto("成员姓名已经存在".encode(), client_addr)
        return

    sk.sendto("ok".encode(),client_addr)
    for i in USER:
        msg = "欢迎新成员" + name
        sk.sendto(msg.encode(),USER[i])

    USER[name] = client_addr



def start():
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sk.bind(ADDR)
    do_request(sk)


if __name__ == "__main__":
    start()
