import os
import sqlite3


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # Попытка использования пути, если мы работаем в PyInstaller Bundle
        base_path = os.path.abspath(".")
        #base_path = sys._MEIPASS
    except Exception:
        # Иначе, мы работаем в обычном Python окружении
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Путь к файлу базы данных внутри скомпилированного исполняемого файла
db_path = resource_path("mydatabase.db")





def get_categories(username):
    with sqlite3.connect(resource_path("mydatabase.db")) as db:
        cursor = db.cursor()
        categories = []
        for row in cursor.execute("SELECT rowid, * FROM texts ORDER BY category"):
            if row[1] not in categories:
                if row[4] == username:
                    categories.append(row[1])
        return categories


def get_names(username):
    with sqlite3.connect(resource_path("mydatabase.db")) as db:
        cursor = db.cursor()
        names = []
        for row in cursor.execute("SELECT rowid, * FROM texts ORDER BY name"):
            if row[4] == username:
                names.append(row[2])
        return names


def get_users():
    with sqlite3.connect(resource_path("mydatabase.db")) as db:
        cursor = db.cursor()
        users = []
        for row in cursor.execute("SELECT rowid, * FROM users ORDER BY name"):
            users.append(str(row[2]).lower())
        print(users)
        return users


def check_password(user):
    with sqlite3.connect(resource_path("mydatabase.db")) as db:
        cursor = db.cursor()
        username = user[0]
        password = user[1]
        try:
            sql = f"SELECT password FROM users WHERE name LIKE '{username}'"
            cursor.execute(sql)
            a = (cursor.fetchall())
            try:
                if password == a[0][0]:
                    return True
            except IndexError:
                pass
        except:
            pass
