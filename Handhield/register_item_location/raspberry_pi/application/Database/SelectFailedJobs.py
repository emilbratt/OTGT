import sqlite3
import os.path as path


def SelectFailedJobs():
    res = False
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = '''
        SELECT id, reg_time, item, shelf, status FROM jobs
        WHERE status = '2'
        AND reg_time < datetime('now', '-7 days')
    '''
    cur.execute(query)
    res = cur.fetchall()
    con.close()
    return res
