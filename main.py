import sqlite3
from PyQt5 import QtWidgets
from Screens import reglog_ui

db = sqlite3.connect('main_db.db')
cursor = db.cursor()

# Create the 'test_login' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_login (
        login TEXT PRIMARY KEY,
        password TEXT
    )
''')
db.commit()

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
        self.setupUi(self)
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

App = QtWidgets.QApplication([])
window = Login()
window.show()
App.exec()
