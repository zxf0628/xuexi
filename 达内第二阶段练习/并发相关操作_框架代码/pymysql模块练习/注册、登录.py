import pymysql


class Entrance:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.db = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user='root',
            password='123',
            database="books",
            charset="utf8mb4"
            # charset="utf-8"
        )

        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def register(self,name,password):
        sql = 'select * from users where name = %s'
        self.cur.execute(sql,[name])
        data = self.cur.fetchall()

        if data:
            return False

        sql = 'insert into users (name,password) values(%s,%s)'
        self.cur.execute(sql,[name,password])
        self.db.commit()
        self.close()
        return True

    def login(self,name,password):
        sql = 'select * from users where name = %s and password = %s '
        self.cur.execute(sql, [name,password])
        data = self.cur.fetchall()

        if data:
            return True


z = Entrance()
# rt = z.register("zxf","123")
rt = z.login("zxf","123")
print(rt)
