import os
import sqlite3
from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtCore import Qt, QEventLoop, QTimer, pyqtSignal
from PyQt5.QtWidgets import QLineEdit

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

    def forgot_password_window(self):
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



class ForgotPasswordWindow(QtWidgets.QMainWindow):
    register_success_signal = pyqtSignal(bool)
    def __init__(self):
        super(ForgotPasswordWindow, self).__init__()
        self.resize(500, 600)
        self.setStyleSheet('background-image: url(":/png/rs/background.png");')

        self.init_ui()

    def init_ui(self):
        self.secret_question_label = QtWidgets.QLabel()
        self.wrong_login_label = QtWidgets.QLabel()


        self.enter_login_label = QtWidgets.QLabel()
        self.enter_login_label.setStyleSheet('font-size: 16pt; color: #856939;')
        self.enter_login_label.setParent(self)
        self.enter_login_label.setAlignment(Qt.AlignCenter)
        self.enter_login_label.show()
        self.enter_login_label.setText('Введите логин')
        self.enter_login_label.setGeometry(0, 300, 500, 30)


        self.fp_login = QLineEdit()
        self.fp_login.setParent(self)
        self.fp_login.setObjectName('passwordEdit')
        self.fp_login.setPlaceholderText(' ' * 15 + 'Логин')
        self.fp_login.setGeometry(150, 360, 200, 30)
        self.username = self.fp_login.text()


        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setObjectName('loginButton')
        self.login_button.setText('Далее...')
        self.login_button.setGeometry(175, 400, 150, 30)



        self.back_to_main_button = QtWidgets.QPushButton('[Выход]')
        self.back_to_main_button.clicked.connect(self.close)
        self.back_to_main_button.setStyleSheet(
            'background-color: #323030; border: none; font: 13pt "Segoe UI"; color: #c29548;')
        self.back_to_main_button.setParent(self)
        self.back_to_main_button.setGeometry(175, 550, 150, 30)

        def check():
            username = self.fp_login.text()
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()

                sql = f"SELECT question FROM users WHERE name LIKE '{username}'"
                cursor.execute(sql)
                self.question = cursor.fetchone()

                if self.question is not None:
                    self.username = self.fp_login.text()
                    self.secret_question_label.setText(self.question[0])
                    self.enter_login_label.hide()
                    self.fp_login.clear()
                    self.login_entered_foo()
                else:
                    print(11)
                    self.enter_login_label.hide()
                    self.fp_login.clear()
                    self.wrong_login_label.setStyleSheet('font-size: 16pt; color: #856939;')
                    self.wrong_login_label.setParent(self)
                    self.wrong_login_label.setAlignment(Qt.AlignCenter)
                    self.wrong_login_label.show()
                    self.wrong_login_label.setText('Неверный логин')
                    self.wrong_login_label.setGeometry(0, 300, 500, 30)

        self.login_button.clicked.connect(check)


    def login_entered_foo(self):
        self.wrong_question_label = QtWidgets.QLabel()
        def check():
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                print(self.username)
                sql = f"SELECT answer FROM users WHERE name LIKE '{self.username}'"
                cursor.execute(sql)
                self.question = cursor.fetchone()

                print(self.secret_answer_edit.text(), self.question)
                if self.question[0].lower() == self.secret_answer_edit.text().lower():
                    self.answer_entered_foo()
                else:
                    self.secret_question_label.hide()
                    self.secret_answer_edit.clear()
                    self.wrong_question_label.setStyleSheet('font-size: 16pt; color: #856939;')
                    self.wrong_question_label.setParent(self)
                    self.wrong_question_label.setAlignment(Qt.AlignCenter)
                    self.wrong_question_label.show()
                    self.wrong_question_label.setText('Неверный ответ')
                    self.wrong_question_label.setGeometry(0, 300, 500, 30)

        self.enter_login_label.hide()
        self.enter_login_label.deleteLater()

        self.wrong_login_label.hide()
        self.wrong_login_label.deleteLater()

        self.fp_login.hide()
        self.fp_login.deleteLater()

        self.login_button.hide()
        self.login_button.deleteLater()

        self.secret_question_label.setStyleSheet('font-size: 16pt; color: #856939;')
        self.secret_question_label.setParent(self)
        self.secret_question_label.setAlignment(Qt.AlignCenter)
        self.secret_question_label.show()
        self.secret_question_label.setGeometry(0, 300, 500, 30)

        self.secret_answer_edit = QLineEdit()
        self.secret_answer_edit.setParent(self)
        self.secret_answer_edit.setStyleSheet('font-size: 13pt;')
        self.secret_answer_edit.setPlaceholderText(' ' * 4 + 'Ваш ответ:')
        self.secret_answer_edit.setGeometry(150, 360, 200, 30)
        self.secret_answer_edit.show()

        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setObjectName('loginButton')
        self.login_button.setText('Далее...')
        self.login_button.setGeometry(175, 400, 150, 30)
        self.login_button.show()
        self.login_button.clicked.connect(check)

    def answer_entered_foo(self):
        self.wrong_question_label.hide()
        self.wrong_question_label.deleteLater()
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            print(self.username)
            sql = f"SELECT password FROM users WHERE name LIKE '{self.username}'"
            cursor.execute(sql)
            self.question = cursor.fetchone()

        self.secret_answer_edit.hide()
        self.secret_answer_edit.deleteLater()

        self.secret_question_label.hide()
        self.secret_question_label.deleteLater()

        self.finish_fp_label = QtWidgets.QLabel()
        self.finish_fp_label.setStyleSheet('font-size: 16pt; color: #856939;')
        self.finish_fp_label.setParent(self)
        self.finish_fp_label.setAlignment(Qt.AlignCenter)
        self.finish_fp_label.show()
        self.finish_fp_label.setText('Ваш пароль:')
        self.finish_fp_label.setGeometry(0, 300, 500, 30)

        self.user_password_edit = QLineEdit()
        self.user_password_edit.setParent(self)
        self.user_password_edit.setText(self.question[0])
        self.user_password_edit.setGeometry(150, 360, 200, 30)
        self.user_password_edit.show()

        self.back_to_main_button = QtWidgets.QPushButton(self)
        self.back_to_main_button.setObjectName('loginButton')
        self.back_to_main_button.setText('Выход')
        self.back_to_main_button.setGeometry(175, 400, 150, 30)
        self.back_to_main_button.show()
        self.back_to_main_button.clicked.connect(self.close)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    file = QtCore.QFile(r"style/style.qss")
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())
    w = RegisterWindow()
    w.show()
    app.exec_()
