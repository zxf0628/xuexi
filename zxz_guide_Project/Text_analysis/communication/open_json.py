import json

class File_data():
    def __init__(self,widget):
        self.widget = widget
        self.file_name = self.widget.ledit_file_path.text()
        self.tedit_show_data = self.widget.tedit_show_data

    def read_data(self):
        path = r"{}".format(self.file_name)
        with open(path,encoding="utf_8")as file:
            data = str(json.load(file))
            self.tedit_show_data.append(data)

