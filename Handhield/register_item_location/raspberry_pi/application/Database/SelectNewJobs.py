import sqlite3
import os.path as path


def SelectNewJobs():
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = '''
        SELECT id, reg_time, item, shelf, status FROM jobs
        WHERE status = '0'
    '''
    cur.execute(query)
    res = cur.fetchall()
    con.close()
    return res
