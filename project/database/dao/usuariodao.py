import sys
sys.path.append('../model/')
from model.usuario import Usuario
from psycopg2 import connect
from dao.dao import DAO

class UsuarioDao(DAO):
    def __init__(self):
        super().__init__()
    
    def buscar(self, usuario):
        try:
            with connect(self._dados_con) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM "usuario" WHERE "login"=%s and "senha"=md5(%s)', [usuario.login, usuario.senha])
                row = cur.fetchone()
                conn.commit()
                cur.close()
                if row == None:
                    return False
                else:
                    usr = Usuario(cod = row[0], nome = row[1], login = row[2])
                    return usr
        except BaseException as e:
            print ("Problema no buscar -- exception seguindo para ser tratada")
            raise e 