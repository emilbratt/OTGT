import sqlite3
import os.path as path


def DeleteAllFailedJobs():
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = '''
        DELETE FROM jobs
        WHERE status = '2'
    '''
    cur.execute(query)
    con.commit()
    con.close()
