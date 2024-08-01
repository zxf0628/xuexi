import socket

s = socket.socket()
s.connect(("127.0.0.1",8888))

f = open("飞书.webp", "rb")

while True:
    data = f.read()
    if not data:
        break
    s.send(data)

f.close()
s.close()