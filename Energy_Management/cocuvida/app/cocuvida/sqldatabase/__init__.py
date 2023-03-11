import sqlite3

DATABASE_FILE = 'data.sqlite'


def connect():
    cnxn = sqlite3.connect(DATABASE_FILE)
    return cnxn
