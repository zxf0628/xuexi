import os
from multiprocessing import Pool, Queue

q = Queue()


def get_catalogue_path():
    base_path = "E:\自下载软件\\"
    catalogue_name = input("请输入要拷贝的目录名：")
    old_folder = base_path + catalogue_name
    print("要拷贝的目录名：", old_folder)
    return old_folder


def copy_file(file, old_folder, new_folder):
    f_r = open(old_folder + "\\" + file, "rb")
    f_w = open(new_folder + "\\" + file, "wb")
    while True:
        data = f_r.read(1024 * 1024)
        if not data:
            break
        n = f_w.write(data)
        q.put(n)

    f_r.close()
    f_w.close()


def main():
    old_folder = get_catalogue_path()
    new_folder = old_folder + "-备份"
    os.mkdir(new_folder)
    all_file = os.listdir(old_folder)

    # 计算目录总大小
    totle_size = 0
    for file in all_file:
        totle_size += os.path.getsize(old_folder + "\\" + file)

    # 进程池分配任务
    pool = Pool()
    for file in all_file:
        pool.apply_async(copy_file, args=(file, old_folder, new_folder))

    pool.close()

    # 显示拷贝进度百分比
    print("目录大小:%.2fM" % (totle_size / 1024 / 1024))
    copy_size = 0
    while True:
        copy_size += q.get()
        print("拷贝了%.1f%%" % (copy_size / totle_size * 100))
        print("zzzzzzzzzzzzzzzzzzzzzzzzzzz")
        # print("拷贝了",copy_size)
        if copy_size >= totle_size:
            break

    pool.join()


if __name__ == "__main__":
    main()
