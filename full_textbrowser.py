import os
import sqlite3
import sys
import threading
import pyglet
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QTextCharFormat, QFont, QTextBlockFormat
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QWidget, QTextBrowser, QVBoxLayout, QHBoxLayout, QAction, QMainWindow
import resources_rc
from sound_zip import get_sound

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # Попытка использования пути, если мы работаем в PyInstaller Bundle
        #base_path = sys._MEIPASS
        base_path = os.path.abspath(".")

    except Exception:
        # Иначе, мы работаем в обычном Python окружении
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Путь к файлу базы данных внутри скомпилированного исполняемого файла
db_path = resource_path("mydatabase.db")
sound_tumbler = True


def type_sound(sound):
    if sound_tumbler:
        song = pyglet.media.load(sound, streaming=False)
        song.play()


def sound_thread_start(sound):
    thread = threading.Thread(target=type_sound, args=(sound,))
    thread.start()


class TextBrowserWidget(QTextBrowser):
    save_text_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_S:
                # noinspection PyUnresolvedReferences
                self.save_text_signal.emit(True)
        if not e.isAutoRepeat():
            if e.key() != Qt.Key_Shift and e.key() != Qt.Key_Control and e.key() != Qt.Key_Alt:
                if e.key() == Qt.Key_Return:
                    # noinspection SpellCheckingInspection
                    sound_thread_start(get_sound('newstring.mp3'))
                if e.key() == Qt.Key_Backspace:
                    sound_thread_start(get_sound('backspace.mp3'))
                else:
                    sound_thread_start(get_sound('type.mp3'))
                QTextBrowser.keyPressEvent(self, e)


class FullTextBrowser(QMainWindow):
    window_closed_signal = pyqtSignal(list)

    def __init__(self, text):
        super().__init__()
        self.main_text_browser = text[1]
        text = text[0]

        with sqlite3.connect(resource_path("mydatabase.db")) as db:
            cursor = db.cursor()
            sql = f"SELECT * FROM texts WHERE name LIKE '{text[1]}'"
            cursor.execute(sql)
            text = (cursor.fetchone())


        self.setObjectName('main')
        self.resize(750, 650)
        self.setMinimumWidth(100)
        self.text = text
        self.text_name = text[1]
        self.text_category = text[0]
        self.content = text[2]
        self._createActions()
        self.main_widget = QWidget()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self._old_pos = None
        self._createToolBars()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.buttons_layout = QHBoxLayout()
        self.text_browser = TextBrowserWidget()
        self.text_browser.save_text_signal.connect(self.save_foo)
        self.text_browser.setReadOnly(False)
        self.text_browser.setObjectName('textBrowser')
        self.text_browser.setHtml(self.main_text_browser.toHtml())

        self.main_layout.addWidget(self.text_browser)
        self.setCentralWidget(self.main_widget)

    def _createToolBars(self):

        self.editToolBar = self.addToolBar("Основное")
        self.editToolBar.setStyleSheet('border: None;')
        self.editToolBar.addAction(self.font_action)
        self.editToolBar.addAction(self.bold_action)
        self.editToolBar.addAction(self.italic_action)
        self.editToolBar.addAction(self.underline_action)
        self.editToolBar.addAction(self.overline_action)
        self.editToolBar.addAction(self.normal_line_action)
        self.editToolBar.addAction(self.center_action)
        self.editToolBar.addAction(self.right_action)
        self.editToolBar.setMovable(False)
        self.editToolBar.setAllowedAreas(Qt.NoToolBarArea)
        self.editToolBar.setContentsMargins(530, 0, 0, 0)

        fileToolBar = self.addToolBar("Текст")
        fileToolBar.setMovable(False)
        fileToolBar.setStyleSheet('border: None;')
        fileToolBar.setAllowedAreas(Qt.NoToolBarArea)
        fileToolBar.addAction(self.save_action)
        fileToolBar.addAction(self.sound_action)
        fileToolBar.addAction(self.close_action)

        self.addToolBar(self.editToolBar)
        self.addToolBar(fileToolBar)

    def _createActions(self):
        self.save_action = QAction(QIcon(":png/rs/save_icon.png"), "Сохранить", self)
        self.save_action.triggered.connect(self.save_foo)
        self.sound_action = QAction(QIcon(":png/rs/sound_on_icon.png"), "Звук", self)
        self.sound_action.triggered.connect(self.sound_switch_foo)
        self.close_action = QAction(QIcon(":png/rs/close_icon.png"), "Закрыть", self)
        self.close_action.triggered.connect(self.close_foo)

        self.font_action = QAction(QIcon(":png/rs/font.png"), "Обычный текст", self)
        self.font_action.triggered.connect(self.normal_font_action)
        self.bold_action = QAction(QIcon(":png/rs/bold.png"), "Жирный текст", self)
        self.bold_action.triggered.connect(self.bold_action_foo)
        self.italic_action = QAction(QIcon(":png/rs/italic.png"), "Курсив", self)
        self.italic_action.triggered.connect(self.italic_action_foo)
        self.underline_action = QAction(QIcon(":png/rs/underline_icon.png"), "Подчеркивание", self)
        self.underline_action.triggered.connect(self.underline_action_foo)
        self.overline_action = QAction(QIcon(":png/rs/overline_icon.png"), "Подчеркивание", self)
        self.overline_action.triggered.connect(self.overline_action_foo)
        self.normal_line_action = QAction(QIcon(":png/rs/lines_icon.png"), "Выравнивание по левому", self)
        self.normal_line_action.triggered.connect(self.normal_line_action_foo)
        self.center_action = QAction(QIcon(":png/rs/center_icon.png"), "Центрирование", self)
        self.center_action.triggered.connect(self.center_action_foo)
        self.right_action = QAction(QIcon(":png/rs/right_icon.png"), "Выравнивание по правому", self)
        self.right_action.triggered.connect(self.right_action_foo)

    def save_foo(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(resource_path("mydatabase.db"))
        db.open()
        query = QSqlQuery()
        query.prepare(f"""
            UPDATE texts 
            SET content = (:content) 
            WHERE name = '{self.text_name}'
        """)
        query.bindValue(":content", self.text_browser.toHtml())
        query.exec()
        db.commit()
        db.close()

    def close_foo(self):
        self.save_foo()
        signal_var = [self.main_text_browser, self.text_name]
        self.window_closed_signal.emit(signal_var)
        self.close()

    def sound_switch_foo(self):
        global sound_tumbler
        if sound_tumbler:
            self.sound_action.setIcon(QIcon(':/sound/rs/sound_off_icon.png'))
            sound_tumbler = False
        else:
            self.sound_action.setIcon(QIcon(':/sound/rs/sound_on_icon.png'))
            sound_tumbler = True

    # noinspection PyAttributeOutsideInit
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    # noinspection PyAttributeOutsideInit
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        # noinspection PyBroadException
        try:
            if not self._old_pos:
                return
            delta = event.pos() - self._old_pos
            self.move(self.pos() + delta)
        except Exception:
            pass

    def bold_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextCharFormat()
        text_char_format.setFontWeight(QFont.Bold)
        cursor.mergeCharFormat(text_char_format)

    def italic_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextCharFormat()
        text_char_format.setFontItalic(True)
        cursor.mergeCharFormat(text_char_format)

    def underline_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextCharFormat()
        text_char_format.setFontUnderline(True)
        cursor.mergeCharFormat(text_char_format)

    def overline_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextCharFormat()
        text_char_format.setFontStrikeOut(True)
        cursor.mergeCharFormat(text_char_format)

    def centering_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextCharFormat()
        text_char_format.setFontWeight(QFont.Bold)
        cursor.mergeCharFormat(text_char_format)

    def normal_font_action(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextCharFormat()
        text_char_format.setFontWeight(QFont.Normal)
        text_char_format.setFontItalic(False)
        text_char_format.setFontUnderline(False)
        text_char_format.setFontStrikeOut(False)
        cursor.mergeCharFormat(text_char_format)

    def center_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextBlockFormat()
        text_char_format.setAlignment(Qt.AlignCenter)
        cursor.mergeBlockFormat(text_char_format)

    def right_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextBlockFormat()
        text_char_format.setAlignment(Qt.AlignRight)
        cursor.mergeBlockFormat(text_char_format)

    def normal_line_action_foo(self):
        cursor = self.text_browser.textCursor()
        text_char_format = QTextBlockFormat()
        text_char_format.setAlignment(Qt.AlignLeft)
        cursor.mergeBlockFormat(text_char_format)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.editToolBar.setContentsMargins(a0.size().width() - 320, 0, 0, 0)
