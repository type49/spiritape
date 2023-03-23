import os
import sqlite3
from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtCore import Qt, QEventLoop, QTimer, pyqtSignal
import db_foo
from db_foo import get_db_path
import resources_rc

db_path = get_db_path()
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users
                  (name TEXT, password TEXT, question Text, answer TEXT)
               """)

conn.commit()
conn.close()

class RegisterWindow(QtWidgets.QMainWindow):
    register_success_signal = pyqtSignal(bool)
    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.resize(500, 600)
        self.setStyleSheet('background-image: url(":/png/rs/background.png");')

        self.init_ui()

    def init_ui(self):
        self.login_label = QtWidgets.QLabel(self)
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_label.setText(' -- Логин -- ')
        self.login_label.setGeometry(150, 190, 200, 30)
        self.login_form = QtWidgets.QLineEdit(self)
        self.login_form.setAlignment(Qt.AlignCenter)
        self.login_form.setGeometry(150, 220, 200, 30)

        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_label.setText(' -- Пароль -- ')
        self.password_label.setGeometry(150, 250, 200, 30)
        self.password_form = QtWidgets.QLineEdit(self)
        self.password_form.setAlignment(Qt.AlignCenter)
        self.password_form.setGeometry(150, 280, 200, 30)

        self.secret_q__label = QtWidgets.QLabel(self)
        self.secret_q__label.setAlignment(Qt.AlignCenter)
        self.secret_q__label.setText('Секретный вопрос:')
        self.secret_q__label.setGeometry(150, 340, 200, 30)
        self.secret_q__form = QtWidgets.QLineEdit(self)
        self.secret_q__form.setAlignment(Qt.AlignCenter)
        self.secret_q__form.setGeometry(100, 370, 300, 30)

        self.secret_a__label = QtWidgets.QLabel(self)
        self.secret_a__label.setAlignment(Qt.AlignCenter)
        self.secret_a__label.setText('Секретный ответ:')
        self.secret_a__label.setGeometry(150, 400, 200, 30)
        self.secret_a__form = QtWidgets.QLineEdit(self)
        self.secret_a__form.setAlignment(Qt.AlignCenter)
        self.secret_a__form.setGeometry(125, 430, 250, 30)


        self.register_button = QtWidgets.QPushButton('Создать')
        self.register_button.setParent(self)
        self.register_button.setGeometry(95, 490, 150, 30)
        self.register_button.clicked.connect(self.create_user)

        self.cancel_button = QtWidgets.QPushButton('Отмена')
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setParent(self)
        self.cancel_button.setGeometry(250, 490, 150, 30)

    def create_user(self):
        if not self.login_form.text():
            wrong_login_label = QtWidgets.QLabel()
            wrong_login_label.setObjectName('wrongLoginLabel')
            wrong_login_label.setParent(self)
            wrong_login_label.setAlignment(Qt.AlignCenter)
            wrong_login_label.show()
            wrong_login_label.setText('Введите логин')
            wrong_login_label.setGeometry(0, 190, 500, 30)
            loop = QEventLoop()
            QTimer.singleShot(1500, loop.quit)
            loop.exec()
            wrong_login_label.close()
            return
        if self.login_form.text().lower() in db_foo.get_users():
            wrong_login_label = QtWidgets.QLabel()
            wrong_login_label.setObjectName('wrongLoginLabel')
            wrong_login_label.setParent(self)
            wrong_login_label.setAlignment(Qt.AlignCenter)
            wrong_login_label.show()
            wrong_login_label.setText('Это имя уже занято.')
            wrong_login_label.setGeometry(0, 190, 500, 30)
            loop = QEventLoop()
            QTimer.singleShot(1500, loop.quit)
            loop.exec()
            wrong_login_label.close()
            return
        if not self.password_form.text():
            wrong_login_label = QtWidgets.QLabel()
            wrong_login_label.setObjectName('wrongLoginLabel')
            wrong_login_label.setParent(self)
            wrong_login_label.setAlignment(Qt.AlignCenter)
            wrong_login_label.show()
            wrong_login_label.setText('Введите пароль')
            wrong_login_label.setGeometry(0, 250, 500, 30)
            loop = QEventLoop()
            QTimer.singleShot(1500, loop.quit)
            loop.exec()
            wrong_login_label.close()
            return
        if not self.login_form.text():
            wrong_login_label = QtWidgets.QLabel()
            wrong_login_label.setObjectName('wrongLoginLabel')
            wrong_login_label.setParent(self)
            wrong_login_label.setAlignment(Qt.AlignCenter)
            wrong_login_label.show()
            wrong_login_label.setText('Задайте секретный вопрос')
            wrong_login_label.setGeometry(0, 340, 500, 30)
            loop = QEventLoop()
            QTimer.singleShot(1500, loop.quit)
            loop.exec()
            wrong_login_label.close()
            return
        if not self.login_form.text():
            wrong_login_label = QtWidgets.QLabel()
            wrong_login_label.setObjectName('wrongLoginLabel')
            wrong_login_label.setParent(self)
            wrong_login_label.setAlignment(Qt.AlignCenter)
            wrong_login_label.show()
            wrong_login_label.setText('Введите ответ')
            wrong_login_label.setGeometry(0, 400, 500, 30)
            loop = QEventLoop()
            QTimer.singleShot(1500, loop.quit)
            loop.exec()
            wrong_login_label.close()
            return
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute(f"""INSERT INTO users
                                              VALUES ('{self.login_form.text()}', '{self.password_form.text()}',
                                               '{self.secret_q__form.text()}', '{self.secret_a__form.text()}')"""
                           )
            db.commit()

        self.register_success_signal.emit(True)
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    file = QtCore.QFile(r"style/style.qss")
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())
    w = RegisterWindow()
    w.show()
    app.exec_()
