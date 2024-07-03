import configparser

class File_data():
    def __init__(self,widget):
        self.widget = widget
        self.file_name = self.widget.ledit_file_path.text()
        self.tedit_show_data = self.widget.tedit_show_data

    def read_data(self):
        path = r"{}".format(self.file_name)
        config = configparser.ConfigParser()
        config.read(path, encoding="utf-8")
        result = str(config.sections())
        self.tedit_show_data.append(result)