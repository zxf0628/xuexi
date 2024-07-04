import glob
import os


def split_list(lst, num_parts):
    length = len(lst)
    part_size = length // num_parts  # 每个部分的大小
    remainder = length % num_parts  # 余数，如果不能整除

    result = []
    start = 0

    for i in range(num_parts):
        if i < remainder:
            end = start + part_size + 1  # 对于有余数的部分，多分配一个元素
        else:
            end = start + part_size

        result.append(lst[start:end])
        start = end

    return result


def avg_dict(mm_split_list):
    section_list = []
    for section in range(len(mm_split_list)):
        section_avg = sum(mm_split_list[section]) / len(mm_split_list[section])
        section_avg_int = round(section_avg, 2)
        section_list.append(section_avg_int)
    return section_list


def find_file():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    files_list = glob.glob(os.path.join(dir_path, "engineer*"))
    return files_list


file_lists = ['E:\\python apply to work\\engineer.2023-11-29 08_41_33 - 副本.log',
              'E:\\python apply to work\\engineer.knee.2024-01-03.13-27-21.log']


def judge_operation_type():
    specified_character = "engineer.knee"
    for f in file_lists:
        if specified_character in f:
            print("6800")
        else:
            print("5800")


def find_root_file():
    root_folder = './'
    file_name_contains = 'engineer'
    file_path_list = []
    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            if file_name_contains in file_name:
                # 文件名符合条件，进行相应操作
                file_path = os.path.join(root, file_name)
                file_path_list.append(file_path)
    return file_path_list


planes = {}
planekey = 2
# oneplane = [1, 2, 3, 4, 5]
# test_list = [6]
oneplane = (1, 2, 3, 4, 5)
test_list = (6,)
planes[planekey] = {"data": oneplane, "flow_data": oneplane}
planes[planekey]["flow_data"]=oneplane+test_list
# planes[planekey]["flow_data"].extend(oneplane)

print(id(planes[planekey]["data"]),id(planes[planekey]["flow_data"]))
