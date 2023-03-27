import sqlite3
import sys
import threading
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QEventLoop, QTimer, Qt, pyqtSignal, QModelIndex, QSize
from PyQt5.QtGui import QStandardItem, QFont, QColor, QStandardItemModel, QMovie, QIcon
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, \
    QLineEdit, QDesktopWidget, QTreeView, QTextBrowser, QComboBox, QInputDialog, \
    QMenu, QMessageBox, QDialog
import pyglet
import db_foo
from db_foo import get_db_path
from sound_zip import get_sound
import register_form
import resources_rc

sound_tumbler = True

db_path = get_db_path()
with sqlite3.connect(db_path) as db:
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS texts
                      (category TEXT, name TEXT, content Text, author TEXT)
                   """)
    db.commit()


def type_sound(sound):
    if sound_tumbler:
        song = pyglet.media.load(sound, streaming=False)
        song.play()


def sound_thread_start(sound):
    thread = threading.Thread(target=type_sound, args=(sound,))
    thread.start()


class SoundButton(QPushButton):

    def __init__(self, icon):
        super().__init__()
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(26, 26))


class LoginEdit(QLineEdit):

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, e):
        if not e.key() in [Qt.Key_Shift, Qt.Key_Control]:
            self.setAlignment(QtCore.Qt.AlignCenter)
            QtWidgets.QLineEdit.keyPressEvent(self, e)
        if self.text() == '':
            self.setAlignment(QtCore.Qt.AlignLeft)


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=10, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()
        fnt = QFont('Segoe UI', font_size)
        fnt.setBold(set_bold)
        self._old_pos = None
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)


class TextBrowser(QTextBrowser):
    change_selection_item_on_tree_signal = pyqtSignal(QModelIndex)
    save_text_signal = pyqtSignal(bool)
    is_hidden = False

    def __init__(self, value):
        super().__init__()
        self.value = value
        self.setPlaceholderText('Click and type for create The Great')

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.change_selection_item_on_tree_signal.emit(self.value)

    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_S:
                self.save_text_signal.emit(True)
        if not e.isAutoRepeat():
            if e.key() != Qt.Key_Shift and e.key() != Qt.Key_Control and e.key() != Qt.Key_Alt:
                if e.key() == Qt.Key_Return:
                    sound_thread_start(get_sound('newstring.mp3'))
                if e.key() == Qt.Key_Backspace:
                    sound_thread_start(get_sound('backspace.mp3'))
                else:
                    sound_thread_start(get_sound('type.mp3'))
                QTextBrowser.keyPressEvent(self, e)

    def focusInEvent(self, e: QtGui.QFocusEvent):
        self.setStyleSheet('background-color: #f5deb3')

    def focusOutEvent(self, ev: QtGui.QFocusEvent):
        self.setStyleSheet('background-color: #dec7a2')

    def save_text_button_click(self, button):
        button.click()


class CreateNewText(QWidget):
    name_and_category_signal = pyqtSignal(list)
    new_category_signal = pyqtSignal(StandardItem)
    cancel_signal = pyqtSignal(bool)

    def __init__(self, username, parent=None):
        self.username = username
        super().__init__(parent, QtCore.Qt.Window)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/png/rs/icon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setFixedSize(400, 200)
        self.setObjectName('createNewTextWindow')
        self.setWindowTitle('Создание Нового')
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.name_for_new_text_edit = QLineEdit()
        self.name_for_new_text_edit.setObjectName('newTextName')

        self.category_layout = QHBoxLayout()
        self.categories = QComboBox()
        self.categories.setObjectName('newTextCategory')
        self.categories.addItems(db_foo.get_categories(self.username))

        self.add_category_button = QPushButton('Добавить тему')
        self.add_category_button.setObjectName('addCategoryButton')
        self.add_category_button.clicked.connect(self.create_new_category)
        self.add_category_button.setFixedSize(150, 30)

        self.category_layout.addWidget(self.categories)
        self.category_layout.addWidget(self.add_category_button)

        self.cancel_button = QPushButton('Отмена')
        self.cancel_button.setObjectName('cancelNewTextButton')
        self.cancel_button.clicked.connect(self.cancel)

        self.create_button = QPushButton('Создать')
        self.create_button.setObjectName('createNewTextButton')
        self.create_button.clicked.connect(self.create_new_text)

        button_layout = QHBoxLayout()

        name_label = QLabel('Название:')
        name_label.setObjectName('label')
        name_label.setFixedHeight(20)
        self.mainLayout.addWidget(name_label)
        self.mainLayout.addWidget(self.name_for_new_text_edit)
        category_label = QLabel('Тема:')
        category_label.setObjectName('label')
        self.mainLayout.addWidget(category_label)
        self.mainLayout.addLayout(self.category_layout)
        self.mainLayout.addSpacing(15)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.create_button)

        self.mainLayout.addLayout(button_layout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)
        self.show()

    def create_new_text(self):
        if self.name_for_new_text_edit.text() not in db_foo.get_names(self.username):
            if self.name_for_new_text_edit.text() != self.categories.currentText():
                print(self.name_for_new_text_edit.text(), self.categories.currentText())
                new_text_category_and_name = [self.categories.currentText(), self.name_for_new_text_edit.text()]
                self.name_and_category_signal.emit(new_text_category_and_name)
                sound_thread_start(get_sound('newlist.mp3'))
            else:
                QMessageBox.warning(self, "Ошибка ", "Название текста не должно совпадать с названием категории.",
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Ошибка ", "Такое уже есть. Давай оригинальнее. ", QMessageBox.Ok)
            self.name_for_new_text_edit.setText('')
            self.name_for_new_text_edit.setFocus()

    def no_users_error_message(self):
        QMessageBox.warning(self, "Ошибка ", "Пользователь не найден. ", QMessageBox.Ok)

    def create_new_category(self):
        self.setWindowOpacity(0.5)
        new_category_dialog = QInputDialog(self)
        new_category_dialog.setWindowFlags(Qt.WindowStaysOnTopHint |
                                           Qt.FramelessWindowHint |
                                           Qt.Window |
                                           Qt.CustomizeWindowHint)
        new_category_dialog.setInputMode(QInputDialog.TextInput)
        new_category_dialog.setLabelText("Name:")
        new_category_dialog.setFixedSize(400, 200)
        ok = new_category_dialog.exec_()
        text = new_category_dialog.textValue()

        if ok:
            if text in db_foo.get_categories(self.username):
                QMessageBox.warning(self, "Ошибка ", "Такая тема уже существует. ", QMessageBox.Ok)
                self.create_new_category()
            else:
                with sqlite3.connect(db_path) as db:
                    cursor = db.cursor()
                    cursor.execute(f"""INSERT INTO texts
                                      VALUES ('{text}', '__49__', '', '{self.username}')"""
                                   )
                    db.commit()

                category = StandardItem(f'{text}', 13, set_bold=True)
                self.categories.addItem(text)
                self.categories.setCurrentText(text)
                self.setWindowOpacity(1)
                self.new_category_signal.emit(category)
        else:
            self.setWindowOpacity(1)

    def cancel(self):
        self.cancel_signal.emit(True)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.create_button.click()


class TreeView(QTreeView):
    delete_item_signal = pyqtSignal(QModelIndex)

    def __init__(self):
        super(TreeView, self).__init__()

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.item_menu = QMenu(self)
        action1 = self.item_menu.addAction('   [Стереть]')
        action1.triggered.connect(self.delete_action)

    def context_menu(self, pos):
        self.selected_index = self.selectedIndexes()
        global_pos = self.viewport().mapToGlobal(pos)
        if len(self.selected_index):
            self.item_menu.exec_(global_pos)

    def delete_action(self):
        def delete_anyway():
            dialog.close()
            self.selected_index = self.selected_index[0]
            sound_thread_start(get_sound('deletelist.mp3'))
            categories = []
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                for row in cursor.execute("SELECT rowid, * FROM texts ORDER BY category"):
                    if row[1] not in categories:
                        categories.append(row[1])
                if str(self.selected_index.data()) not in categories:
                    sql = f"DELETE FROM texts WHERE name = '{self.selected_index.data()}'"
                    cursor.execute(sql)
                    db.commit()
                else:
                    sql = f"DELETE FROM texts WHERE category = '{self.selected_index.data()}'"
                    cursor.execute(sql)
                    db.commit()
            self.delete_item_signal.emit(self.selected_index)

        dialog = QDialog()
        dialog.setStyleSheet('background-color: #323030;')
        dialog.setWindowFlag(Qt.FramelessWindowHint)
        dialog.setFixedSize(300, 150)
        label = QtWidgets.QLabel('Вы уверены? \n Восстановление будет невозможно.')
        label.setStyleSheet('color: #CDBEA7; font: 13pt "Segoe UI";')
        label.setParent(dialog)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, 300, 100)
        ok_btn = QPushButton('Да.', dialog)
        ok_btn.clicked.connect(delete_anyway)
        ok_btn.setStyleSheet('background-color: #CDBEA7;')
        ok_btn.setGeometry(30, 90, 100, 25)
        cancel_btn = QPushButton('Нет.', dialog)
        cancel_btn.clicked.connect(dialog.close)
        cancel_btn.setStyleSheet('background-color: #CDBEA7;')
        cancel_btn.setGeometry(170, 90, 100, 25)
        dialog.setWindowTitle("Dialog")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


class MainWindow(QWidget):
    key_switcher = ''
    sound_button_signal = pyqtSignal(QPushButton)
    save_button_signal = pyqtSignal(QPushButton)

    def __init__(self):
        super().__init__()
        self.register_success_label = QLabel()
        self.setWindowTitle('[Spiritape]')
        self.setObjectName('main')
        self.resize(500, 600)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/png/rs/icon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)

        self.centering_window()
        self.forgot_pass_button = QtWidgets.QPushButton('[Забыл пароль]')

        self.login_ui()

    def login_ui(self):
        self.wrong_login_count = 0
        self.key_switcher = 'login'
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.setFixedSize(500, 600)

        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, -20, 500, 500)
        self.movie = QMovie(':gif/rs/spiritape.gif')
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        self.login_edit = LoginEdit()
        self.login_edit.setParent(self)
        self.login_edit.resize(200, 30)
        self.login_edit.move(150, 370)
        self.login_edit.setObjectName('loginEdit')
        self.login_edit.setPlaceholderText(' ' * 15 + 'Логин')
        self.login_edit.setGeometry(150, 370, 200, 30)

        self.password_edit = LoginEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setParent(self)
        self.password_edit.setObjectName('passwordEdit')
        self.password_edit.setPlaceholderText(' ' * 15 + 'Пароль')
        self.password_edit.setGeometry(150, 410, 200, 30)

        self.login_button = QPushButton(self)
        self.login_button.setObjectName('loginButton')
        self.login_button.setText('Войти')
        self.login_button.setGeometry(175, 460, 150, 30)
        self.login_button.clicked.connect(self.enter_foo)



        self.register_button = QtWidgets.QPushButton('[Регистрация]')
        self.register_button.clicked.connect(self.register_window)
        self.register_button.setStyleSheet(
            'background-color: #323030; border: none; font: 13pt "Segoe UI"; color: #c29548;')
        self.register_button.setParent(self)
        self.register_button.setGeometry(175, 570, 150, 30)

        self.exit_button = QtWidgets.QPushButton('[Выход]')
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet(
            'background-color: #323030; border: none; font: 13pt "Segoe UI"; color: #c29548;')
        self.exit_button.setParent(self)
        self.exit_button.setGeometry(175, 550, 150, 30)

    def enter_foo(self):
        self.wrong_login = QLabel(self)
        self.wrong_login.setObjectName('wrongLoginLabel')
        db_foo.check_password([self.login_edit.text(), self.password_edit.text()])
        if db_foo.check_password([self.login_edit.text(), self.password_edit.text()]):
            self.username = self.login_edit.text()
            self.register_button.hide()
            self.register_button.deleteLater()
            self.exit_button.hide()
            self.exit_button.deleteLater()
            self.forgot_pass_button.hide()
            self.forgot_pass_button.deleteLater()
            self.login_edit.hide()
            self.login_edit.deleteLater()
            self.password_edit.deleteLater()
            self.password_edit.hide()
            self.login_button.hide()
            self.login_button.deleteLater()
            if self.wrong_login.isVisible():
                self.wrong_login.hide()
            if self.register_success_label.isVisible():
                self.register_success_label.close()

            self.gif_label.hide()
            self.movie.deleteLater()
            self.gif_label.deleteLater()
            self.wrong_login.deleteLater()

            self.setMaximumSize(99999, 99999)
            _old_window_width = 500
            while _old_window_width < 800:
                self.resize(_old_window_width, 500)
                _old_window_width += 20
                self.centering_window()
                loop = QEventLoop()
                QTimer.singleShot(1, loop.quit)
                loop.exec()

            self.main_ui()
        else:
            self.wrong_login_count += 1
            print(self.wrong_login_count)
            if self.wrong_login_count > 2:
                print(11)
                self.forgot_pass_button.clicked.connect(self.forgot_password_window)
                self.forgot_pass_button.setStyleSheet(
                    'background-color: #323030; border: none; text-decoration: blink; font: 13pt "Segoe UI"; color: #ff294d;')
                self.forgot_pass_button.setParent(self)
                self.forgot_pass_button.setGeometry(175, 530, 150, 30)
                self.forgot_pass_button.show()
            self.login_edit.setAlignment(Qt.AlignLeft)
            self.password_edit.setAlignment(Qt.AlignLeft)
            self.login_edit.setText('')
            self.password_edit.setText('')
            self.login_edit.setFocus()
            self.wrong_login.setAlignment(Qt.AlignCenter)
            self.wrong_login.show()
            self.wrong_login.setText('Неверные данные')
            self.wrong_login.setGeometry(0, 320, 500, 30)
            loop = QEventLoop()
            QTimer.singleShot(700, loop.quit)
            loop.exec()
            self.wrong_login.close()

    def main_ui(self):
        self.key_switcher = 'entered'
        self.mainbox = QHBoxLayout()
        self.mainbox.setAlignment(Qt.AlignLeft)

        self.treebox = QVBoxLayout()

        self.tree_view = TreeView()
        self.tree_view.delete_item_signal.connect(self.update_tree_view)
        self.tree_view.setObjectName('treeView')
        self.tree_view.setFixedWidth(200)
        self.tree_view.setHeaderHidden(True)

        self.tree_model = QStandardItemModel()
        self.root_node = self.tree_model.invisibleRootItem()

        for i in db_foo.get_categories(self.username):
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                sql = f"SELECT * FROM texts WHERE category LIKE '{i}'"
                cursor.execute(sql)
                a = (cursor.fetchall())
                if a:
                    category_item = StandardItem(a[0][0], 13, set_bold=True)
                    for text in a:
                        text_name = text[1]
                        if text_name != '__49__':
                            text_item = StandardItem(text_name, 12)
                            category_item.appendRow(text_item)
                    self.root_node.appendRow(category_item)

        self.tree_view.doubleClicked.connect(self.text_manager)
        self.tree_view.setModel(self.tree_model)
        self.tree_view.expandAll()

        new_text_button = QPushButton('Новый текст')
        new_text_button.setObjectName('newTextButton')
        new_text_button.clicked.connect(self.create_window)

        exit_button = QPushButton('❌')
        exit_button.setObjectName('closeAppButton')
        exit_button.clicked.connect(self.close)

        sound_button = SoundButton(':/png/rs/sound_on_icon.png')

        sound_button.setObjectName('soundButton')
        sound_button.clicked.connect(lambda ch, w=sound_button: self.off_sound(w))

        technical_buttons_box = QHBoxLayout()
        technical_buttons_box.addWidget(sound_button)
        technical_buttons_box.addWidget(exit_button)

        self.treebox.addWidget(self.tree_view, 1)
        self.treebox.addWidget(new_text_button)
        self.treebox.addLayout(technical_buttons_box)
        self.treebox.setContentsMargins(0, 0, 0, 9)

        self.mainbox.addLayout(self.treebox)

        self.setLayout(self.mainbox)

    def text_manager(self, value):
        if value.data() not in db_foo.get_categories(self.username):
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                sql = f"SELECT * FROM texts WHERE name LIKE '{value.data()}'"
                cursor.execute(sql)
                a = (cursor.fetchone())
                text = a[2]

                def save_text():
                    text_content = text_browser.toHtml()
                    name = a[1]
                    query = f"UPDATE texts SET content = ? WHERE name = ?"
                    cursor.execute(query, (text_content, name))
                    db.commit()
                    db.close()

                def close_tb():
                    save_text()
                    self.mainbox.removeWidget(browser_widget)
                    text_browser.deleteLater()
                    tbclosebtn.deleteLater()
                    tbsavebtn.deleteLater()
                    tbopenbtn.deleteLater()
                    tblayout.deleteLater()


            text_browser = TextBrowser(value)
            text_browser.save_text_signal.connect(save_text)
            text_browser.setObjectName('textBrowser')
            text_browser.change_selection_item_on_tree_signal.connect(self.set_focus_on_tree)
            text_browser.setReadOnly(False)
            text_browser.setText(text)

            buttonlayout = QHBoxLayout()

            tbclosebtn = QPushButton('☒')
            tbclosebtn.setObjectName('tbclosebutton')
            tbsavebtn = QPushButton('☑')
            tbsavebtn.setObjectName('tbsavebutton')
            tbopenbtn = QPushButton('☐')
            tbopenbtn.setObjectName('tbopenbutton')

            buttonlayout.addWidget(tbopenbtn)
            buttonlayout.addWidget(tbsavebtn)
            buttonlayout.addWidget(tbclosebtn)

            browser_widget = QWidget()
            tblayout = QVBoxLayout(browser_widget)

            tblayout.addLayout(buttonlayout)
            tblayout.addWidget(text_browser)
            self.mainbox.addWidget(browser_widget, 1)
            tbclosebtn.clicked.connect(close_tb)
            _fullscreen_var = [a, text_browser]
            tbopenbtn.clicked.connect(lambda ch, w=_fullscreen_var: self.fullscreen_textbrowser(w))
            tbsavebtn.clicked.connect(save_text)

    def create_window(self):
        self.setWindowOpacity(0.7)
        self.creating_new_text_window = CreateNewText(self.username, self)
        self.creating_new_text_window.cancel_signal.connect(self.cancel_creating)
        self.creating_new_text_window.show()
        self.creating_new_text_window.name_and_category_signal.connect(self.create_new_text)
        self.creating_new_text_window.new_category_signal.connect(self.update_tree_view)

    def create_new_text(self, data):
        new_text = [(data[0], data[1], '', self.username), ]
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.executemany("INSERT INTO texts VALUES (?,?,?,?)", new_text)
            db.commit()
            sql = "DELETE FROM texts WHERE name = ''"
            cursor.execute(sql)
            db.commit()

        file_item = StandardItem(f'{data[1]}', 12)

        self.tree_model.findItems(f'{data[0]}', Qt.MatchRecursive | Qt.MatchExactly)[0].appendRow(file_item)
        self.tree_view.setCurrentIndex(self.tree_model.indexFromItem(file_item))

        self.creating_new_text_window.close()
        self.setWindowOpacity(1)

        self.text_manager(self.tree_view.currentIndex())

    def update_tree_view(self, data):
        if type(data) != StandardItem:
            if data.data() not in db_foo.get_categories(self.username):
                data_search_result = self.tree_model.findItems(
                    f'{data.parent().data()}', Qt.MatchExactly)
                if data_search_result:
                    data_search_result[0].removeRow(data.row())
                else:
                    self.root_node.removeRow(data.row())
            else:
                self.root_node.removeRow(data.row())
        else:
            self.root_node.appendRow(data)

    def cancel_creating(self):
        self.creating_new_text_window.close()
        self.setWindowOpacity(1)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return and self.key_switcher == 'login':
            self.login_button.click()
        if e.key() == QtCore.Qt.Key_Escape and self.key_switcher == 'login':
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        try:
            if not self._old_pos:
                return
            delta = event.pos() - self._old_pos
            self.move(self.pos() + delta)
        except Exception:
            pass

    def centering_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def set_focus_on_tree(self, value):
        self.tree_view.setCurrentIndex(value)

    def off_sound(self, button):
        global sound_tumbler
        if sound_tumbler:
            button.setIcon(QIcon(':/png/rs/sound_off_icon.png'))
            sound_tumbler = False
        else:
            button.setIcon(QIcon(':/png/rs/sound_on_icon.png'))
            sound_tumbler = True

    def fullscreen_textbrowser(self, text):

        import full_textbrowser
        textbrowser = text[1]
        textbrowser.setStyleSheet('background-color: #95918c')
        textbrowser.setReadOnly(True)
        textbrowser.setEnabled(False)
        _to_fullscreen = [text]
        self.full_tb = full_textbrowser.FullTextBrowser(text)
        self.full_tb.show()
        self.full_tb.window_closed_signal.connect(self.textbrowser_unlock)
        query = QSqlQuery()
        query.prepare(f"""
                UPDATE texts 
                SET content = (:content) 
                WHERE name = '{text[0][1]}'
                """)
        query.bindValue(":content", textbrowser.toHtml())
        query.exec()

    def textbrowser_unlock(self, signal_var):
        print('unlocked')
        text_name = signal_var[1]
        textbrowser = signal_var[0]
        textbrowser.setStyleSheet('background-color: #dec7a2')
        textbrowser.setReadOnly(False)
        textbrowser.setEnabled(True)
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM texts WHERE name LIKE '{text_name}'")
            a = (cursor.fetchone())
            print(a)
            text = a[2]
            print(text)
            textbrowser.setText(text)

    def register_window(self):
        self.key_switcher = 'register'
        self.register_form = register_form.RegisterWindow()

        self.register_form.setParent(self)

        self.register_form.show()
        self.register_form.register_success_signal.connect(self.register_success)

    def forgot_password_window(self):
        self.key_switcher = 'forgot_password'
        self.forgot_password_form = register_form.ForgotPasswordWindow()

        self.forgot_password_form.setParent(self)

        self.forgot_password_form.show()
        self.forgot_password_form.register_success_signal.connect(self.register_success)

    def register_success(self):
        self.key_switcher = 'login'
        self.register_success_label.setStyleSheet('background-color: #42ff9e;')
        self.register_success_label.setObjectName('wrongLoginLabel')
        self.register_success_label.setParent(self)
        self.register_success_label.setAlignment(Qt.AlignCenter)
        self.register_success_label.show()
        self.register_success_label.setText('Регистрация завершена. Введите свои данные.')
        self.register_success_label.setGeometry(0, 320, 500, 35)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    file = QtCore.QFile(r":/qss/style/style.qss")
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
