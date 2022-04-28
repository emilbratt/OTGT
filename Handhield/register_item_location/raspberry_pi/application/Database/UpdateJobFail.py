import sqlite3
import os.path as path


def UpdateJobFail(id):
    id = id
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = '''
        UPDATE jobs
        SET status = '2'
        WHERE id = :id
    '''
    cur.execute(query, {'id': id} )
    con.commit()
    con.close()
