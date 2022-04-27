import sqlite3
import os.path as path


# if database file does not exist, this script will create it and its tables
class StartDatabase:

    def __init__(self):
        print('this is StartDatabase')
        self.dir = path.dirname(path.realpath(__file__))
        self.db = path.join(self.dir, 'data.sqlite')
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()
        self.create_table_jobs()
        self.con.commit()
        self.con.close()


    def create_table_jobs(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS jobs
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reg_time DATE DEFAULT (DATETIME('now','localtime')),
                barcode INTEGER,
                shelf TEXT,
                status TEXT
            )
        ''')
