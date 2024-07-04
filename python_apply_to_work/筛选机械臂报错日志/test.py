class Percon():
    def __init__(self,name):
        self.name = name


    def __str__(self):
        super().__str__()
        super(Percon, self).__str__()
        return "现在我是老大咯"



p = Percon("zxf")
print(dir(p))
print(p)