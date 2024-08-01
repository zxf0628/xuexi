import pymysql
import re

db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user='root',
    password='123',
    database="books",
    charset="utf8mb4"
    # charset="utf-8"
)

cur = db.cursor()

# 存头像
f = open("曹操.jpg","rb")
data = f.read()

sql = 'update sanguo set img = %s where name = "曹操"'
cur.execute(sql,data)
db.commit()

# 取头像
sql = 'select img from sanguo where id = 1'
cur.execute(sql)
data = cur.fetchone()[0]

with open("./奸雄.jpg","wb")as f:
    f.write(data)

# 查看函数获取数据的准确类型及格式
sql = 'select id from sanguo'
cur.execute(sql)
data = cur.fetchall()
print(data[0][0])


cur.close()
db.close()