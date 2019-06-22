import sys
sys.path.append('../model/')
from model.user import User
from psycopg2 import connect
from dao.dao import DAO

class UserDao(DAO):
    def __init__(self):
        super().__init__()
    
    def register(self, user):
        try:
            with connect(self._dados_con) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO "user" ("name", "nickname", "password", "mail") VALUES (%s, %s, %s, %s)', [user.name, user.nickname, user.password, user.mail])
                conn.commit()
                cur.close()
                return True
        except BaseException as e:
            print ("Fail in register")
            raise e
    
    def login(self, user):
        try:
            with connect(self._dados_con) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM "user" WHERE "nickname"=%s', [user.nickname])
                row = cur.fetchone()
                conn.commit()
                cur.close()
                if row == None:
                    return False
                else:
                    user = User(cod = row[0], name = row[1], nickname = row[2], password = row[3], mail = row[4])
                    user.verify = row[5]
                    user.admin = row[6]
                    return user
        except BaseException as e:
            print ("Fail in login")
            raise e
    
    def verifyuser(self, user):
        try:
            with connect(self._dados_con) as conn:
                cur = conn.cursor()
                cur.execute('SELECT "nickname", "mail" FROM "user" WHERE "nickname"=%s OR "mail"=%s', [user.nickname, user.mail])
                row = cur.fetchone()
                conn.commit()
                cur.close()
                if row == None:
                    return False
                else:
                    error = []
                    if row[0] == user.nickname:
                        error.append(1)
                    if row[1] == user.mail:
                        error.append(4)
                    return error
        except BaseException as e:
            print ("Fail in search")
            raise e

    def doverify(self, user):
        try:
            with connect(self._dados_con) as conn:
                cur = conn.cursor()
                cur.execute('UPDATE "user" SET "verify" = True WHERE "cod" = %s;', [user.cod])
                conn.commit()
                cur.close()
                return True
        except BaseException as e:
            print ("Fail in search")
            raise e