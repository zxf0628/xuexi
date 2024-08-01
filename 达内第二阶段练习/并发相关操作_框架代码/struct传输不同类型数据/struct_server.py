import socket
import struct

st = struct.Struct("i32sif")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
s.bind(("127.0.0.1", 8882))

f = open("student_info.txt", "a")

while True:
    data,addr = s.recvfrom(1024)
    data = st.unpack(data)

    info = "%d %-10s %d %.1f\n" % (data[0], data[1].decode().strip("\x00"), data[2], data[3])
    f.write(info)
    f.flush()
    print(":",info)
