import sqlite3
import os.path as path


def DeleteJob(id):
    dir = path.dirname(path.realpath(__file__))
    db = path.join(dir, 'data.sqlite')
    con = sqlite3.connect(db)
    cur = con.cursor()
    query = '''
        DELETE FROM jobs
        WHERE id = :id
    '''
    cur.execute(query, {'id': id} )
    con.commit()
    con.close()
