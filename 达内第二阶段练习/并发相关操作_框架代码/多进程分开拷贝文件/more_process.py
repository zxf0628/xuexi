from multiprocessing import Process
import os

filename = "th.jfif"
filesize = os.path.getsize(filename)


def get_top():
    fr = open(filename, 'rb')
    fw = open("top.jpg", "wb")
    n = filesize // 2
    fw.write(fr.read(n))
    fr.close()
    fw.close()


def get_bot():
    fr = open(filename, 'rb')
    fw = open("bot.jpg", "wb")
    fr.seek(filesize // 2, 0)
    fw.write(fr.read())
    fr.close()
    fw.close()


def start():
    p1 = Process(target=get_top)
    p2 = Process(target=get_bot)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    start()
