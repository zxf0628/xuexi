import os
import re

from chardet.universaldetector import UniversalDetector


class Extraction_Data():
    def __init__(self):
        self.file_path_list = []

    '''遍历该脚本，文件夹与子文件夹，符合指定名称文件
    return:符合筛选条件文件的路径'''

    def find_root_file(self, name, root_folder='./'):
        root_folder = root_folder
        file_name_contains = name
        # file_name_contains = 'engineer'
        file_path_list = []
        for root, dirs, files in os.walk(root_folder):
            for file_name in files:
                if file_name_contains in file_name:
                    # 文件名符合条件，进行相应操作
                    file_path = os.path.join(root, file_name)
                    file_path_list.append(file_path)
        print(file_path_list)
        self.file_path_list = file_path_list

    '''判断文件的编码类型
    return:一个包含文件类型的字典 键为encoding'''

    def detectEncoding(self, file_name):
        bigdata = open(file_name, 'rb')
        detector = UniversalDetector()
        for line in bigdata.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        bigdata.close()
        return detector.result

    '''读取log,拿指定数据'''

    def read_log(self, file_name):
        detres = self.detectEncoding(file_name)
        print(detres)

        content = open(file_name, 'rb').read()

        log_lines = content.decode(encoding=detres['encoding'], errors='ignore').splitlines()

        error_line = []
        for ln in log_lines:
            if "[ERROR : " in ln:
                error_line.append(ln)
        print("error_line:" + str(len(error_line)) + str(error_line))

        for ln in error_line:
            if "HoldingCurrent" in ln:
                axles = self.matching_data(ln)
                print("过流轴：" + axles)
            if "Maximum torque" in ln:
                axles = self.matching_data(ln)
                print("超力矩轴：" + axles)
            if "velocity has been exceeded" in ln:
                axles = self.matching_data(ln)
                print("超速轴：" + axles)

    '''匹配报错日志内的"()"中信息'''

    def matching_data(self, ln):
        pattern = r'\((.*?)\)'
        data = re.search(pattern, ln).group(1)
        return data

    def run(self):
        for i in self.file_path_list:
            self.read_log(i)


zxf = Extraction_Data()
zxf.find_root_file("engineer")
zxf.run()
