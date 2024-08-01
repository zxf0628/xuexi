import logging.config
import pymysql
import hashlib

logging.config.fileConfig("../log_package/logginga.conf")
logger = logging.getLogger()


def change_password(password):
    hash = hashlib.md5()
    hash.update(password.encode())
    return hash.hexdigest()


class Entrance:
    def __init__(self):
        self.initialize()

    def initialize(self):
        logger.debug('Entrance---initialize')
        self.db = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user='root',
            password='123',
            database="dict",
            charset="utf8mb4"
            # charset="utf-8"
        )

    def create_cursor(self):
        logger.debug('Entrance---create_cursor')
        self.cur = self.db.cursor()

    def close_cursor(self):
        logger.debug('Entrance---close_cursor')
        self.cur.close()

    def close(self):
        logger.debug('Entrance---close')
        self.db.close()

    def register(self, name, password):
        logger.debug('Entrance---register---%s--%s' % (name,password))
        sql = 'select name from users where name = %s'
        self.cur.execute(sql, [name])
        data = self.cur.fetchall()
        if data:
            return False

        sql = 'insert into users (name,password) values(%s,%s)'
        try:
            password = change_password(password)
            self.cur.execute(sql, [name, password])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, password):
        logger.debug('Entrance---login---%s %s' % (name, password))
        sql = 'select * from users where name = %s and password = %s '
        password = change_password(password)
        self.cur.execute(sql, [name, password])
        data = self.cur.fetchall()

        if data:
            return True
        else:
            return False

    def select_word(self, name, word):
        logger.debug('Entrance---select_word---%s--%s' % (name,word))
        sql = 'select mean from words where word = %s'
        self.cur.execute(sql, [word])
        word_mean = self.cur.fetchone()[0]
        print('word_mean:', word_mean)

        if word_mean:
            return word_mean
        else:
            return False

    def select_hist(self,name):
        logger.debug('Entrance---select_word---%s' % name)
        sql = 'select name,word,time from ' \
              'where name = %s ' \
              'order by time desc limit 10'
        self.cur.execute(sql, [name])
        hists = self.cur.fetchall()

        return hists

    def insert_hist(self, name, word):
        logger.debug('Entrance---insert_hist---%s--%s' % (name, word))
        sql = 'insert into hist(name,word) values(%s,%s)'
        self.cur.execute(sql, [name, word])
        self.db.commit()