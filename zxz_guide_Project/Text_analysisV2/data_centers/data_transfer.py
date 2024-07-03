# class Singleton:
#     _instance = None
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(Singleton,cls).__new__(cls)
#         return cls._instance

def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kwagrs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwagrs)
        return _instance[cls]

    return _singleton


@Singleton
class Data_Center():
    def __init__(self):
        self.default_content = 0
        self.row_number = self.default_content
        self.col_number = self.default_content

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_row_number(self):
        return self.row_number

    def set_row_number(self, row_number):
        if row_number == "":
            row_number = self.default_content
        self.row_number = row_number

    def get_col_number(self):
        return self.col_number

    def set_col_number(self, col_number):
        if col_number == "":
            col_number = self.default_content
        self.col_number = col_number

# b = Data_Center()
# print("b方法获得路径：{}".format(b.get_file_path()))
# print(id(b.get_file_path()))
# print("b属性获得路径：{}".format(b.file_path))
# print(id(b.file_path))
# print(id(b))
# print("------------------------------------------")
#
#
# a = Data_Center()
# a.set_file_path("cde")
# print("a方法获得路径：{}".format(a.get_file_path()))
# print(id(a.get_file_path()))
# print("a属性获得路径：{}".format(a.file_path))
# print(id(a.file_path))
# print(id(a))
# print("------------------------------------------")
#
#
# c = Data_Center()
# print("c方法获得路径：{}".format(c.get_file_path()))
# print(id(c.get_file_path()))
# print("c属性获得路径：{}".format(c.file_path))
# print(id(c.file_path))
# print(id(c))
