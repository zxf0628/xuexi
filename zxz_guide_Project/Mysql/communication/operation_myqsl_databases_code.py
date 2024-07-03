import pymysql

from PyQt5.QtCore import *
from Mysql.data_centers.data_transfer import Data_Center
from Universal_Methods.Universal_Method import Common_Method


class Processing(QObject):
    _databases_name = pyqtSignal(str)
    _datalabel_name = pyqtSignal(str)
    _datalabel_column_name = pyqtSignal(str)
    _present_data = pyqtSignal(str)
    _statusBar = pyqtSignal(str)

    def __init__(self):
        super(Processing, self).__init__()
        self.data_centre = Data_Center()
        self.connect_databases()
        self.column_name = None

    def connect_databases(self):
        try:
            self.conn = pymysql.connect(host="127.0.0.1", user="root", password="123", charset="utf8mb4")
            self.cursor = self.conn.cursor()

        except Exception as e:
            abnormal = "异常；{}".format(e)
            self._statusBar.emit(abnormal)
            self.conn.close()

        finally:
            self._statusBar.emit("数据库打开成功")

    def initalize_select_database(self):
        databases_name = self.data_centre.get_databases_name()
        self.connect_databases()
        sql1 = "use {}".format(databases_name)
        self.run_sql(sql1)

    def run_sql(self, sql):
        self.cursor.execute(sql)

    def delete_sql(self):
        self.initalize_select_database()
        try:
            label_name = self.data_centre.get_datalabel_name()
            value = self.data_centre.get_delete_condition_value()
            key = self.data_centre.get_delete_condition_key()
            operator = self.data_centre.get_delete_condition_operator()

            wheres = "{keys}{operators}\"{vlaues}\"".format(keys=key, operators=operator, vlaues=value)
            sql = "delete from {} where {}".format(label_name, wheres)
            self.run_sql(sql)
            self.conn.commit()
            self.sin_set_hint_singal_to_statusBar("删除成功")
        except:
            self.sin_set_hint_singal_to_statusBar("删除失败")
        self.conn.close()

    def select_sql(self):
        self.initalize_select_database()

        label_name = self.data_centre.get_datalabel_name()
        value = self.data_centre.get_select_condition_value()
        key = self.data_centre.get_select_condition_key()
        operator = self.data_centre.get_select_condition_operator()
        if value is None:
            self.sin_set_hint_singal_to_statusBar("查询条件未填写")
            self.conn.close()
            return
        wheres = "{keys}{operators}\"{vlaues}\"".format(keys=key,
                                                 operators=operator,
                                                 vlaues=value)
        print("查询条件：{}".format(wheres))
        sql = "select * from {label_name} where {where}".format(label_name=label_name, where=wheres)
        self.run_sql(sql)

        result = self.cursor.fetchall()
        if result:
            print("查询结果处理后字符串：{}".format(str(result)))
            self.sin_set_present_data(str(result))
            self.sin_set_hint_singal_to_statusBar("查询成功")
        else:
            self.sin_set_hint_singal_to_statusBar("未查询到符合条件结果")

        self.conn.close()

    # 将数据反馈到UI控件上的 信号
    def sin_set_present_data(self, data_text):
        self._present_data.emit(str(data_text))

    def sin_set_databases_name(self, databases_name):
        self._databases_name.emit(databases_name)

    def sin_set_datalabel_name(self, datalabel_name):
        self._datalabel_name.emit(datalabel_name)

    def sin_set_datalabel_column_name(self, datalabel_column_name):
        print("处理代码界面列名数据类型：{}".format(type(datalabel_column_name)))
        self._datalabel_column_name.emit(datalabel_column_name)

    def sin_set_hint_singal_to_statusBar(self, singal):
        self._statusBar.emit(str(singal))

    # ui界面按下控件  处理代码界面做相应的处理
    def ui_button_show_databases_name(self):
        self.run_sql("show databases")
        result = self.cursor.fetchall()
        s1 = Common_Method.typle_transition_to_str(result)
        print("库{}".format(s1))
        print(result)
        self.sin_set_databases_name(str(s1))

    def ui_butthon_select_databases_name(self):
        databases_name = self.data_centre.get_databases_name()
        sql = "use {}".format(databases_name)
        self.run_sql(sql)

        # 获取所选择数据库下的所有数据表，并返回给UI界面
        self.run_sql("show tables")
        result = self.cursor.fetchall()
        s1 = Common_Method.typle_transition_to_str(result)
        print("表：{}".format(s1))
        self._datalabel_name.emit(str(s1))

        if result: self.conn.close()

    def ui_button_select_datalabel_name(self):
        datalabel_name = self.data_centre.get_datalabel_name()
        self.initalize_select_database()

        sql2 = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{}\' ORDER BY ORDINAL_POSITION;".format(
            datalabel_name)
        self.run_sql(sql2)

        result = self.cursor.fetchall()
        self.column_name = Common_Method.typle_transition_to_str(result)
        print("表列名:{}".format(self.column_name))
        self.sin_set_datalabel_column_name(self.column_name)
        self.data_centre.set_label_column_name(self.column_name)
        print("表列名类型:{}".format(type(self.column_name)))


        if result: self.conn.close()

    def ui_butthon_to_load_all_data(self):
        self.initalize_select_database()

        try:
            datalabel_name = self.data_centre.get_datalabel_name()
            sql = "select * from {};".format(datalabel_name)
            self.run_sql(sql)
            results = self.cursor.fetchall()
            self.sin_set_present_data(str(results))
            if results:return results

        except:
            self.sin_set_hint_singal_to_statusBar("加载数据失败")

        self.conn.close()

    def ui_butthon_save_data(self, data):
        self.initalize_select_database()

        try:
            label_name = self.data_centre.get_datalabel_name()
            sql = "delete from {};".format(label_name)
            self.run_sql(sql)
            for key, value in data.items():
                sql = "insert into {label_name}({cloumn_name}) values('{sid}','{name}','{sex}','{age}','{grade}');".format(
                    sid=key, name=value[0], sex=value[1], age=value[2], grade=value[3],label_name=label_name,cloumn_name=self.column_name)
                self.run_sql(sql)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as z:
            print("处理代码界面的保存数据异常：{}".format(z))
            return False
