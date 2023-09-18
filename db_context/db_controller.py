import sqlite3
from sqlite3 import *


class DB:
    def __init__(self):
        self.con = sqlite3.connect('../main_db.db')
        self.cursor = self.con.cursor()

    def login(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0:
            return

        if len(user_password) == 0:
            return

        self.cursor.execute(f'SELECT password FROM users WHERE login="{user_login}"')
        check_pass = self.cursor.fetchall()

        self.cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
        check_login = self.cursor.fetchall()

        if check_pass[0][0] == user_password and check_login[0][0] == user_login:
            self.label.setText('Успешная авторизация!')
        else:
            self.label.setText('Ошибка авторизации!')
        self.cursor.close()
        self.con.close()

    def reg(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0:
            return

        if len(user_password) == 0:
            return

        self.cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
        if self.cursor.fetchone() is None:
            self.cursor.execute(f'INSERT INTO users VALUES ("{user_login}", "{user_password}")')
            self.label.setText(f'Аккаунт {user_login} успешно зарегистрирован!')
            self.con.commit()
        else:
            self.label.setText('Такая записать уже имеется!')
        self.cursor.close()
        self.con.close()