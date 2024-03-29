import sqlite3
import os.path as path


def SelectJobsToday():
    res = False
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = '''
        SELECT id, reg_time, item, shelf, status FROM jobs
        WHERE reg_time
        BETWEEN DATETIME("now", "start of day")
        AND DATETIME("now", "localtime")
    '''
    cur.execute(query)
    res = cur.fetchall()
    con.close()
    return res
