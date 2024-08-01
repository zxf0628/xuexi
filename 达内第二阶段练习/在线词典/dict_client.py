import socket
import getpass
import logging.config
import sys

logging.config.fileConfig("../log_package/logginga.conf")
logger = logging.getLogger()

# 全局变量
HOST = "127.0.0.1"
PORT = 8886
ADDR = (HOST, PORT)

S = socket.socket()
S.connect(ADDR)


def send_info(info):
    logger.debug("---send_info---%s" % info)
    S.send(info.encode())


def recv_info():
    info = S.recv(1024).decode()
    logger.debug("---recv_info---%s" % info)
    return info


def do_register():
    while True:
        name = input('用户名：')
        password = getpass.getpass('密码：')
        logger.debug("---do_register---%s--%s" % (name,password))

        if name == 'E' or password == 'E':
            break

        if " " in name or " " in password:
            print("用户名与密码中不能包含空格")
            continue

        info = 'R %s %s' % (name, password)
        send_info(info)
        feedback_info = recv_info()
        if feedback_info == 'OK':
            print('注册成功')
            interface(name)
        else:
            print(feedback_info)


def do_login():
    while True:
        name = input('用户名：')
        password = getpass.getpass('密码：')
        logger.debug("---do_login---%s  %s" % (name, password))

        if name == 'E' or password == 'E':
            break

        if " " in name or " " in password:
            print("用户名与密码中不能包含空格")
            continue

        info = 'L %s %s' % (name, password)
        send_info(info)
        feedback_info = recv_info()
        if feedback_info == 'OK':
            interface(name)
        else:
            print(feedback_info)


def do_select_word(name):
    while True:
        word = input("请输入要查询的单词：")

        if word == 'E':
            break

        if " " in word:
            print("用户名与密码中不能包含空格")
            continue

        info = 'S %s %s' % (name,word)
        send_info(info)
        feedback_info = recv_info()
        print(feedback_info)


def do_select_hist(name):
    info = 'H %s' % (name)
    send_info(info)
    data = recv_info()
    if data == 'OK':
        while True:
            data = recv_info()
            if data == '##':
                break
            print(data)
    else:
        print('没有历史记录')


def interface(name):
    while True:
        print("""
        =============================
        S 查单词    H 查看记录    E 注销
        =============================
        """)
        command = input("要进行的操作：")
        if command == "S":
            do_select_word(name)
        elif command == 'H':
            do_select_hist(name)
        elif command == 'E':
            return


def main():
    logger.debug("main---主循环")
    while True:
        print("""
        =========================
        L 登录    R 注册    E 退出
        =========================
        """)
        command = input("要进行的操作：")
        if command == "L":
            do_login()
        elif command == 'R':
            do_register()
        elif command == 'E':
            send_info('E')
            sys.exit('客户端进程退出')


if __name__ == "__main__":
    main()