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

args_list = []
f = open("3 四级-乱序.txt",encoding="utf-8")
for line in f:
    # word,mean = line.split("  ",1)
    word,mean = re.split(r'\s+',line,1)
    args_list.append((word,mean.strip()))


sql = 'insert into words (word,word_explain) values (%s,%s)'.format(word,mean)
sql = 'insert into words (word,word_explain) values (%s,%s)'

cur.executemany(sql,args_list)
db.commit()


cur.close()
db.close()