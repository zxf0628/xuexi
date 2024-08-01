import socket

def request(client_socket_obj):
    data = client_socket_obj.recv(4646)
    if not data:
        return

    request_line = data.decode().split("\n")[0]
    info = request_line.split(" ")[1]

    if info == "/":
        # with open("../线程进程小章训练/服务器接收http1/index.html")as f:
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "<h1>加油加油雄起</h1>"
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "<h1>Sorry.....</h1>"

    client_socket_obj.send(response.encode())


sockfd = socket.socket()
sockfd.bind(("127.0.0.1",8888))
sockfd.listen(3)
while True:
    client_socket_obj,addr = sockfd.accept()
    request(client_socket_obj)

