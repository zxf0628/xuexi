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
        self.select_condition_value = None
        self.delete_condition_value = None

    def get_databases_name(self):
        return self.databases_name

    def set_databases_name(self, databases_name):
        self.databases_name = databases_name

    def get_datalabel_name(self):
        return self.datalabel_name

    def set_datalabel_name(self, datalabel_name):
        self.datalabel_name = datalabel_name

    def get_select_condition_operator(self):
        return self.select_condition_operator

    def set_select_condition_operator(self, condition):
        self.select_condition_operator = condition

    def get_select_condition_key(self):
        return self.select_condition_key

    def set_select_condition_key(self, key):
        self.select_condition_key = key

    def get_select_condition_value(self):
        return self.select_condition_value

    def set_select_condition_vlaue(self, value):
        self.select_condition_value = value

    def get_delete_condition_operator(self):
        return self.delete_condition_operator

    def set_delete_condition_operator(self, condition):
        self.delete_condition_operator = condition

    def get_delete_condition_key(self):
        return self.delete_condition_key

    def set_delete_condition_key(self, key):
        self.delete_condition_key = key

    def get_delete_condition_value(self):
        return self.delete_condition_value

    def set_sdelete_condition_vlaue(self, value):
        self.delete_condition_value = value

    def get_label_column_name(self):
        return self.column_name

    def set_label_column_name(self, column_name=[]):
        self.column_name = column_name
