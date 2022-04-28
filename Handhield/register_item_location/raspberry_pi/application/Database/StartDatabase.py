import sqlite3
import os.path as path


def StartDatabase():
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = '''
        CREATE TABLE IF NOT EXISTS jobs
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_time DATE DEFAULT (DATETIME('now','localtime')),
            item INTEGER,
            shelf TEXT,
            status TEXT
        )
    '''
    cur.execute(query)
    con.commit()
    con.close()
