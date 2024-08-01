import socket

s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
s.bind(("127.0.0.1",8888))
s.listen(3)
client_socket,addr= s.accept()


f = open("嗨嗨嗨.webp", "wb")

while True:
    data = client_socket.recv(1024)
    if not data:
        break
    f.write(data)

f.close()
s.close()
