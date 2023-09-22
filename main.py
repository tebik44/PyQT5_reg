import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from Screens import reglog_ui, table_dialog

db = sqlite3.connect('main_db.db')
cursor = db.cursor()

class Registration(QtWidgets.QMainWindow, reglog_ui.Ui_MainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Регистрация')
        self.lineEdit.setPlaceholderText('Введите Логин')
        self.lineEdit_2.setPlaceholderText('Введите Пароль')
        self.pushButton.setText('Регистрация')
        self.pushButton_2.setText('Вход')
        self.setWindowTitle('Регистрация')

        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.login)

    def login(self):
        self.login_window = Login()
        self.login_window.show()
        self.hide()

    def reg(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0 or len(user_password) == 0:
            self.label.setText('Поля не могут быть пустыми!')
            return

        cursor.execute('SELECT login FROM test_login WHERE login=?', (user_login,))
        existing_login = cursor.fetchone()

        if existing_login is None:
            cursor.execute('INSERT INTO test_login (login, password) VALUES (?, ?)', (user_login, user_password))
            db.commit()
            self.label.setText(f'Аккаунт {user_login} успешно зарегистрирован!')
        else:
            self.label.setText('Такая запись уже существует!')

class Login(QtWidgets.QMainWindow, reglog_ui.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Screens/reglog.ui', self)
        # self.setupUi(self)
        self.label.setText('')
        self.label_2.setText('Логин')
        self.lineEdit.setPlaceholderText('Введите логин')
        self.lineEdit_2.setPlaceholderText('Введите пароль')
        self.pushButton.setText('Вход')
        self.pushButton_2.setText('Регистрация')
        self.setWindowTitle('Вход')

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.reg)

    def reg(self):
        self.reg_window = Registration()
        self.reg_window.show()
        self.hide()

    def login(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0 or len(user_password) == 0:
            self.label.setText('Поля не могут быть пустыми!')
            return

        cursor.execute('SELECT password FROM test_login WHERE login=?', (user_login,))
        stored_password = cursor.fetchone()

        if stored_password is not None and stored_password[0] == user_password:
            self.label.setText('Успешная авторизация!')
        else:
            self.label.setText('Ошибка авторизации!')


class Table(QtWidgets.QMainWindow, table_dialog.Ui_MainWindow):
    def __init__(self):
        super(Table, self).__init__()
        self.setupUi(self)

        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.loaddata()

    def loaddata(self):
        cursor.execute("""
            select * from test_login
        """
        )
        names = list(map(lambda x: x[0], cursor.description))
        dict = cursor.fetchall()
        self.tableWidget.setRowCount(len(names))
        self.tableWidget.setColumnCount(len(names))

        # Заполните ячейки таблицы данными из базы данных
        for row_index, row_data in enumerate(dict):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)








if __name__ == '__main__':
    App = QtWidgets.QApplication([])
    window = Table()
    window.show()
    App.exec()
