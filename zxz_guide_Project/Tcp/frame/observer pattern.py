# 抽象 订阅者（观察者）
class Observer():
    def update(self,subject):
        pass

# 抽象 发布者（被观察者、主体对象)
class Subject():
    def __init__(self):
        self.observers = []

    def add_obs(self,obs):
        self.observers.append(obs)

    def del_obs(self,obs):
        self.observers.remove(obs)

    def notify(self):
        for obs in self.observers:
            obs.update(self)


# 具体 发布者
class Staff_Suject(Subject):
    def __init__(self,company_info=None):
        super(Staff_Suject, self).__init__()
        self.__company_info = company_info

    @property
    def company_info(self):
        return self.__company_info

    @company_info.setter
    def company_info(self,new_company_info):
        self.__company_info = new_company_info
        self.notify()

# 具体 订阅者
class Staff(Observer):
    def __init__(self):
        super(Observer,self).__init__()
        self.company_info = None

    def update(self,subject):
        self.company_info = subject.company_info

"""对观察者模式理解：
1.触发发布者同步订阅者消息的原理是：将发布者变量设置为私有变量，想要修改变量 要调用声明的方法 当方法调用后紧接着执行通告方法
2.抽象订阅者，下只需有一个修改数据方法，形参是等待传入发布者父类对象的实参,从而拿到发布者下的变量
3.发布者的指定变量一旦修改，同时将管理的全部订阅者变量进行更新，是调用父类发布者 下早定义好的方法 
  通告方法内容：遍历具体订阅者实例对象 并运行订阅者实例对象下的 更新数据方法
4.是否不需要这种子类继承父类，一个抽象一个具体类？
5.如果只有一个具体订阅者类，也可以实现这个简单的观察者模式？
6.任何类与类之间是否都可以使用种同步的方法？是只要将这个最基本的属性方法写入就可以？

"""

company = Staff_Suject("初始化公司消息")
staff1 = Staff()
staff2 = Staff()
company.add_obs(staff1)
company.add_obs(staff2)
print(company.company_info)
print(staff1.company_info)
company.company_info = "放假，放假，就是放假！！！"
print(staff1.company_info)