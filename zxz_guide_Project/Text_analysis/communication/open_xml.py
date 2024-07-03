from xml.etree import ElementTree as ET

class File_data():
    def __init__(self,widget):
        self.widget = widget
        self.file_name = self.widget.ledit_file_path.text()
        self.tedit_show_data = self.widget.tedit_show_data

    def read_data(self):
        path = r"{}".format(self.file_name)
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            print(child.tag, child.attrib)
            self.tedit_show_data.append(str(child.tag))
            self.tedit_show_data.append(str(child.attrib))
            for node in child:
                print(node.tag, node.attrib, node.text)
                self.tedit_show_data.append(str(node.tag))
                self.tedit_show_data.append( str(node.attrib))
                self.tedit_show_data.append(str(node.text))


