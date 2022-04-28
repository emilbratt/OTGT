import sqlite3
import os.path as path

# this will insert jobs (barcode and shelf value) for the daemon to handle

def InsertJob(data):
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''
        INSERT INTO jobs
        (
            item, shelf, status
        )
        VALUES
        (
            :item, :shelf, :status
        )
    ''', data)
    con.commit()
    con.close()
