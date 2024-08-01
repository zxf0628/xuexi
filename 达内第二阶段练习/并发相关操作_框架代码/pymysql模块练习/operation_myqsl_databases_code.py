import pymysql

from MysqlV2.data_centers.data_transfer import Data_Center
from Universal_Methods.Universal_Method import Common_Method
from MysqlV2.singal_centers.signal_transfer import Signal_Center


class Processing:
    def __init__(self):
        self.data_centre = Data_Center()
        self.signal_center = Signal_Center()
        self.connect_databases()
        self.column_name = None

    # 连接数据库
    def connect_databases(self):
        print("Processing->connect_databases->")
        try:
            self.conn = pymysql.connect(host="127.0.0.1", user="root", password="123", charset="utf8mb4")
            self.cursor = self.conn.cursor()

        except Exception as reason:
            self.sin_set_hint_singal_to_statusBar("异常:" + str(reason))
            self.conn.close()
            print("异常：Processing->connect_databases->{}".format(reason))

    # 选择要操作的数据库
    def initalize_select_database(self):
        databases_name = self.data_centre.get_databases_name()
        self.connect_databases()
        sql1 = "use {}".format(databases_name)
        print("Processing->initalize_select_database->sql1")
        self.run_sql(sql1)

    # 传入mysql语句，根据创建的pymysql实例对象的游标 运行语句
    def run_sql(self, sql):
        print("Processing->run_sql->sql语句：{}".format(sql))
        self.cursor.execute(sql)

    # 加载全部数据
    def load_all_data(self):
        self.initalize_select_database()
        print("Processing->load_all_data->")

        try:
            datalabel_name = self.data_centre.get_datalabel_name()
            sql = "select * from {};".format(datalabel_name)
            self.run_sql(sql)
            results = self.cursor.fetchall()
            self.sin_set_present_data(str(results))
            if results:
                return results
        except Exception as reason:
            self.sin_set_hint_singal_to_statusBar("加载数据失败")
            print("异常：Processing->load_all_data->{}".format(reason))

        self.conn.close()

    # 保存数据
    def save_data(self, data):
        self.initalize_select_database()
        print("Processing->save_data->")

        try:
            label_name = self.data_centre.get_datalabel_name()

            sql = "delete from {};".format(label_name)
            self.run_sql(sql)
            for key, value in data.items():
                sql = "insert into {label_name}({cloumn_name}) values('{sid}','{name}','{sex}','{age}','{grade}');" \
                    .format(sid=key, name=value[0], sex=value[1], age=value[2],
                            grade=value[3], label_name=label_name, cloumn_name=self.column_name)
                self.run_sql(sql)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as reason:
            print("异常：Processing->save_data->{}".format(reason))
            return False

    # 触发信号中心中已经声明好的 用途信号 并传数据
    def sin_set_present_data(self, data_text):
        self.signal_center.trigger_present_data(data_text)
        print("Processing->sin_set_present_data->：{}".format(data_text))

    def sin_set_databases_name(self, databases_name):
        self.signal_center.trigger_databases_name(databases_name)
        print("Processing->sin_set_databases_name->：{}".format(databases_name))

    def sin_set_datalabel_name(self, datalabel_name):
        self.signal_center.trigger_datalabel_name(datalabel_name)
        print("Processing->sin_set_datalabel_name->：{}".format(datalabel_name))

    def sin_set_datalabel_column_name(self, datalabel_column_name):
        self.signal_center.trigger_datalabel_column_name(datalabel_column_name)
        print("Processing->sin_set_datalabel_column_name->：{}".format(datalabel_column_name))

    def sin_set_hint_singal_to_statusBar(self, singal):
        self.signal_center.trigger_statusBar(singal)
        print("Processing->sin_set_hint_singal_to_statusBar->：{}".format(singal))

    # ui界面触发控件的自带信号  因在主逻辑界面绑定了该槽函数  运行相对应的函数
    def ui_button_show_databases_name(self):
        print("Processing->ui_button_show_databases_name->")

        self.run_sql("show databases")
        result = self.cursor.fetchall()
        print("Processing->ui_button_show_databases_name->运行sql返回值元组类型:{}".format(result))
        str_result = Common_Method.typle_transition_to_str(result)
        print("Processing->ui_button_show_databases_name->运行sql返回值元组类型转换为字符类型:{}".format(str_result))
        self.sin_set_databases_name(str(str_result))

    def ui_button_select_databases_name(self):
        print("Processing->ui_butthon_select_databases_name->")

        databases_name = self.data_centre.get_databases_name()
        sql = "use {}".format(databases_name)
        self.run_sql(sql)

        # 获取所选择数据库下的所有数据表，并返回给UI界面
        self.run_sql("show tables")
        result = self.cursor.fetchall()
        str_result = Common_Method.typle_transition_to_str(result)
        print("Processing->ui_butthon_select_databases_name->运行sql返回值元组类型转换为字符类型:{}".format(str_result))
        self.sin_set_datalabel_name(str(str_result))

        if result:
            self.conn.close()

    def ui_button_select_datalabel_name(self):
        print("Processing->ui_button_select_datalabel_name->")
        datalabel_name = self.data_centre.get_datalabel_name()
        self.initalize_select_database()

        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{}\' ORDER BY ORDINAL_POSITION;".format(
            datalabel_name)
        self.run_sql(sql)
        result = self.cursor.fetchall()
        self.column_name = Common_Method.typle_transition_to_str(result)
        print("Processing->ui_button_select_datalabel_name->运行sql返回值元组类型转换为字符类型:{}".format(self.column_name))
        self.sin_set_datalabel_column_name(self.column_name)

        if result:
            self.conn.close()

    def ui_button_delete_sql(self):
        self.initalize_select_database()
        print("Processing->ui_button_delete_sql->")

        try:
            label_name = self.data_centre.get_datalabel_name()
            value = self.data_centre.get_delete_condition_value()
            key = self.data_centre.get_delete_condition_key()
            operator = self.data_centre.get_delete_condition_operator()

            wheres = "{keys}{operators}\"{vlaues}\"".format(keys=key, operators=operator, vlaues=value)
            print("Processing->ui_button_delete_sql->删除条件:{}".format(wheres))
            sql = "delete from {} where {}".format(label_name, wheres)
            self.run_sql(sql)
            self.conn.commit()
            self.sin_set_hint_singal_to_statusBar("删除成功")
        except Exception as reason:
            self.sin_set_hint_singal_to_statusBar("删除失败")
            print("异常：Processing->ui_button_delete_sql->{}".format(reason))

        self.conn.close()

    def ui_button_select_sql(self):
        self.initalize_select_database()
        print("Processing->ui_button_select_sql->")

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
        print("Processing->ui_button_select_sql->查询条件:{}".format(wheres))
        sql = "select * from {label_name} where {where}".format(label_name=label_name, where=wheres)
        self.run_sql(sql)
        result = self.cursor.fetchall()

        if result:
            print("Processing->ui_button_select_sql->查询接受到的数据:{}".format(result))
            self.sin_set_present_data(str(result))
            self.sin_set_hint_singal_to_statusBar("查询成功")
        else:
            self.sin_set_hint_singal_to_statusBar("未查询到符合条件结果")

        self.conn.close()

