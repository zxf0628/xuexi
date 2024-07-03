def Singleton(cls):
    _instance={}
    def _singleton(*args,**kwagrs):
        if cls not in  _instance:
            _instance[cls]=cls(*args,**kwagrs)
        return _instance[cls]
    return _singleton

@Singleton
class Data_Center():
    def __init__(self):
        self.target = "广播"

    def set_ip(self,ip):
        self.ip = ip

    def get_ip(self):
        return self.ip


    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port


    def set_host_name(self, host_name):
        self.host_name = host_name

    def get_host_name(self):
        return self.host_name


    def set_connect_num(self, connect_num):
        self.connect_num = connect_num

    def get_connect_num(self):
        return self.connect_num


    def set_select_target(self,target):
        self.target = target

    def get_select_target(self):
        return self.target