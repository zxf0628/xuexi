import os
import re
from openpyxl import Workbook

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


    def get_sum(self,file_name):
        detres = self.detectEncoding(file_name)
        print(detres)

        content = open(file_name, 'rb').read()

        log_lines = content.decode(encoding=detres['encoding'], errors='ignore').splitlines()

        error_line = []
        for ln in log_lines:
            if "System.currentTimeMillis() - oldSysTime" in ln:
                error_line.append(ln)
        print("error_line:" + str(len(error_line)) + str(error_line))

        sum_list = []
        for ln in error_line:
            data = self.matching_data(ln)
            sum_list.append(data)
        print("数据样式",sum_list[0:10])
        return sum_list

    '''匹配报错日志内的"()"中信息'''

    def matching_data(self, ln):
        pattern = r"oldSysTime = (\d+)"

        # 在文本中搜索匹配的内容
        data = re.search(pattern, ln).group(1)
        if data:
            return data

    def print_excel(self,sum_list):
        wb = Workbook()

        # 选择要操作的工作表
        ws = wb.active

        # 定义要插入的列表数据

        # 将列表数据插入到Excel的第一列中
        for index, value in enumerate(sum_list, start=1):
            # 在第一列中写入数据
            ws.cell(row=index, column=1, value=value)

        # 保存Excel文件
        wb.save("example.xlsx")

    def run(self):
        for i in self.file_path_list:
            sum_list = self.get_sum(i)
            sum_list = [int(i) for i in sum_list]
            self.print_excel(sum_list)


zxf = Extraction_Data()
zxf.find_root_file("Project")
zxf.run()
