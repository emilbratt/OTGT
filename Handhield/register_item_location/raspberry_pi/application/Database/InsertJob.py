import sqlite3
import os.path as path

# this will insert jobs (barcode and shelf value) for the daemon to handle

class InsertJob:

    def __init__(self, data: dict):
        self.data = data
        self.dir = path.dirname(path.realpath(__file__))
        self.db = path.join(self.dir, 'data.sqlite')
        self.insert_job()

    def insert_job(self):
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()
        self.cur.execute('''
            INSERT INTO jobs
            (
                item, shelf, status
            )
            VALUES
            (
                :item, :shelf, :status
            )
        ''', self.data)
        self.con.commit()
        self.con.close()
