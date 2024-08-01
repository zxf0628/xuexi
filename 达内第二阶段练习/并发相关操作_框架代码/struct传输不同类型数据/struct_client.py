import socket
import struct

st = struct.Struct("i32sif")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("127.0.0.1", 8888)

while True:
    print("===============")
    id = int(input("ID:"))

    name = input('Name:').encode()
    age = int(input("Age:"))
    score = float(input('Score:'))

    info = st.pack(id,name,age,score)

    s.sendto(info,addr)


