import sqlite3
import os.path as path


class SelectJobsToday:

    def __init__(self):
        print('this is SelectJobsToday')
        self.res = False
        self.dir = path.dirname(path.realpath(__file__))
        self.db = path.join(self.dir, 'data.sqlite')
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()
        self.select_jobs_today()
        self.con.close()

    def select_jobs_today(self):
        query = '''
            SELECT * FROM jobs
            WHERE reg_time
            BETWEEN DATETIME("now", "start of day")
            AND DATETIME("now", "localtime")
        '''
        self.cur.execute(query)
        self.res = self.cur.fetchall()
