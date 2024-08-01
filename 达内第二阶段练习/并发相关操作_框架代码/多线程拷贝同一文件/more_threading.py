import sys
from threading import Thread, Lock
import os

lock = Lock()

urls = [
    "E:\A_python_project\Project_Exercise\python_grow\多线程练习文件\A",
    "E:\A_python_project\Project_Exercise\python_grow\多线程练习文件\B",
    "E:\A_python_project\Project_Exercise\python_grow\多线程练习文件\C",
    "E:\A_python_project\Project_Exercise\python_grow\多线程练习文件\D",
]

filename = input("要下载的文件名称：")
print("filename",filename)

explorer = []

for i in urls:
    filepath = i + "\\" + filename
    print(filepath)
    if os.path.exists(filepath):
        explorer.append(filepath)

path_num = len(explorer)
if path_num == 0:
    sys.exit(0)
    # os._exit(0)

file_size = os.path.getsize(explorer[0])
block_size = file_size // path_num

fw = open(filename,"wb")


def load(path,num):
    f = open(path,"rb")
    seek_num = block_size * (num)
    f.seek(seek_num)
    data = f.read(block_size)
    with lock:
        fw.seek(seek_num)
        fw.write(data)



num = 0
jobs = []
for path in explorer:
    t = Thread(target=load,args=(path,num))
    jobs.append(t)
    t.start()
    num += 1

for i in jobs:
    i.join()

