import os
import sqlite3

def get_db_path():
    db_name = 'mydatabase.db'
    appdata_path = os.path.join(os.getenv('APPDATA'), 'spiritape')
    db_path = os.path.join(appdata_path, db_name)
    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)
    return db_path

db_path = get_db_path()

def get_categories(username):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        categories = []
        for row in cursor.execute("SELECT rowid, * FROM texts ORDER BY category"):
            if row[1] not in categories:
                if row[4] == username:
                    categories.append(row[1])
        return categories


def get_names(username):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        names = []
        for row in cursor.execute("SELECT rowid, * FROM texts ORDER BY name"):
            if row[4] == username:
                names.append(row[2])
        return names


def get_users():
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        users = []
        for row in cursor.execute("SELECT rowid, * FROM users ORDER BY name"):
            users.append(str(row[2]).lower())
        return users


def check_password(user):
    with sqlite3.connect(db_path) as db:
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

def check_secret_answer(user):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        username = user[0]
        password = user[1]
        try:
            sql = f"SELECT answer FROM users WHERE name LIKE '{username}'"
            cursor.execute(sql)
            a = (cursor.fetchall())
            try:
                if password == a[0][0]:
                    return True
            except IndexError:
                pass
        except:
            pass