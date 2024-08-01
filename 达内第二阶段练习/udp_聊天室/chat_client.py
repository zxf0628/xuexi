import socket

ADDR = ("127.0.0.1",8888)


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        name = input("请输入你的姓名：")
        msg = "L" + "@@@" + name
        s.sendto(msg.encode(),ADDR)

        data,addr = s.recvfrom(1024)
        if data.decode() == "ok":
            print("连接服务器成功")
        else:
            print(data.decode())





if __name__ == "__main__":
    start()