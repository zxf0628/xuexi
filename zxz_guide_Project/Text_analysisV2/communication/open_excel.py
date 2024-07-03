import pandas as pd

from Text_analysisV2.data_centers.data_transfer import Data_Center
from Text_analysisV2.signal_centers.signal_transfer import Signal_Center


class File_data:
    def __init__(self):
        super(File_data, self).__init__()
        self.data_center = Data_Center()
        self.signal_center = Signal_Center()
        self.logsdata = None
        self.initialize_data()

    def initialize_data(self):
        file_path = self.data_center.get_file_path()
        self.logsdata = pd.read_excel(file_path, sheet_name="logs")
        print("File_data->initialize_data->打开文件路径：{}".format(file_path))

    def initialize_row_and_col_to_ui(self):
        print("File_data->initialize_row_and_col_to_ui->")
        rows_and_cols = str(self.logsdata.shape)
        self.sin_send_rowcol(rows_and_cols)
        self.sin_send_signal("打开文件成功")

    def read_data(self):
        column_name = self.logsdata.columns
        column_names = column_name.tolist()
        rows = self.data_center.get_row_number()
        cols = self.data_center.get_col_number()
        print("File_data->read_data->行号：{} 列号：{}".format(rows, cols))

        if rows != 0 and cols != 0:
            data = self.logsdata.iloc[int(rows) - 1, int(cols)]
            set_data = "@@@".join(["row_and_col", str(data)])
            print("File_data->read_data->文本处理代码row_and_col返回数据：{}".format(set_data))
            self.sin_send_text(set_data)

        elif rows != 0 and cols == 0:
            pandas_data = self.logsdata.iloc[int(rows) - 1].values
            tolist_data = pandas_data.tolist()

            set_data = "@@@".join(["row", str(tolist_data), str(column_names)])
            print("File_data->read_data->文本处理代码row返回数据：{}".format(set_data))
            self.sin_send_text(set_data)

        elif rows == 0 and cols != 0:
            pandas_data = self.logsdata[str(column_names[int(cols)])].values
            tolist_data = pandas_data.tolist()
            column_names = column_names[int(cols)]

            set_data = "@@@".join(["col", str(tolist_data), str(column_names)])
            print("File_data->read_data->文本处理代码col返回数据：{}".format(set_data))
            self.sin_send_text(set_data)

        elif rows == 0 and cols == 0:
            pandas_data = self.logsdata.iloc[:, :].values
            tolist_data = pandas_data.tolist()

            set_data = "@@@".join(["all", str(tolist_data), str(column_names)])
            print("File_data->read_data->文本处理代码all返回数据{}".format(set_data))
            self.sin_send_text(set_data)

        else:
            self.sin_send_signal("输入行列号异常")
            self.sin_send_rowcol("输入行列号异常")

    def sin_send_text(self, text):
        print("File_data->sin_send_text->:{}".format(text))
        self.signal_center.trigger_text(text)

    def sin_send_signal(self, signal):
        print("File_data->sin_send_signal->:{}".format(signal))
        self.signal_center.trigger_signal(signal)

    def sin_send_rowcol(self, row_and_col):
        print("File_data->sin_send_rowcol->:{}".format(row_and_col))
        self.signal_center.trigger_row_and_col(row_and_col)

