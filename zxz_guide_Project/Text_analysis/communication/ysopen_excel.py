import pandas as pd
from PyQt5.QtCore import *
from Text_analysis.data_centers import Text_parsing_control as D_C


class File_data(QObject):
    _text = pyqtSignal(str)
    _signal = pyqtSignal(str)
    _rowcol = pyqtSignal(str)

    def __init__(self):
        super(File_data, self).__init__()
        self.widget = D_C.Data_Center()
        self.initialize_data()

    def initialize_data(self):
        file_path = self.widget.get_file_path()
        print("打开文件{}".format(file_path))
        self.logsdata = pd.read_excel(file_path, sheet_name="logs")


    def initialize_data_to_ui(self):
        self.rows_cols = str(self.logsdata.shape)
        self.send_rowcol(self.rows_cols)
        self.send_signal("打开文件成功")


    def read_data(self):
        column_name = self.logsdata.columns
        column_names = column_name.tolist()
        rows = self.widget.get_row_number()
        cols = self.widget.get_col_number()
        print("文件处理类读数据行号{}，列号{}".format(rows,cols))

        if rows != 0 and cols != 0:
            data = self.logsdata.iloc[int(rows)-1,int(cols)]
            set_data = "@@@".join(["row_and_col",str(data)])
            print("文本处理代码row_and_col返回数据：{}".format(set_data))
            self.send_text(set_data)

        elif rows!= 0 and cols == 0:
            pandas_data = self.logsdata.iloc[int(rows)-1].values
            tolist_data = pandas_data.tolist()

            set_data = "@@@".join(["row", str(tolist_data),str(column_names)])
            print("文本处理代码row返回数据：{}".format(set_data))
            self.send_text(set_data)

        elif rows == 0 and cols != 0:
            pandas_data = self.logsdata[str(column_names[int(cols)])].values
            tolist_data = pandas_data.tolist()
            column_names = column_names[int(cols)]

            set_data = "@@@".join(["col",str(tolist_data),str(column_names)])
            print("文本处理代码col返回数据：{}".format(set_data))
            self.send_text(set_data)

        elif rows == 0 and cols == 0:
            pandas_data = self.logsdata.iloc[:,:].values
            tolist_data = pandas_data.tolist()

            set_data = "@@@".join(["all", str(tolist_data),str(column_names)])
            print("全部数据要反馈给ui界面的列名{}".format(set_data))
            self.send_text(set_data)

        else:
            self.send_signal("输入行列号异常")



    def send_text(self,text):
        self._text.emit(text)
        print("发射信号，传递内容{}".format(text))

    def send_signal(self,signal):
        self._signal.emit(signal)
        print("发射信号，反馈状态栏{}".format(signal))

    def send_rowcol(self,rowcol):
        self._rowcol.emit(rowcol)
        print("发射信号，反馈行列数{}".format(rowcol))



