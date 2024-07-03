class Notice:
    def __init__(self):
        self.ob = []

    def attach(self,ob):
        self.ob.append(ob)

    def notify(self):
        for ob in self.ob:
            ob.update(self)


class StaffNotice(Notice):
    def __init__(self,company_info=None):
        super().__init__()
        self.__company_info = company_info

    @property
    def company_info(self):
        return self.__company_info

    @company_info.setter
    def company_info(self,info):
        self.__company_info = info


obj = StaffNotice("zZZ")
print(obj.company_info)