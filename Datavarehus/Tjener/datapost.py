import mariadb
import sys
from writelog import Log
from postqueries import *

'''
year            INT             NOT NULL,
monthly         INT             NOT NULL,
date            INT             NOT NULL,
week            INT             NOT NULL,
week_day        VARCHAR(255)    NOT NULL,
yyyymmdd        INT             NOT NULL,
'''



class Postconnect:
    def __init__(self):
        from credentials import loadCredentials
        credentials = loadCredentials('post')

        try:
            self.cnxn = mariadb.connect(
                user=credentials['user'],
                password=credentials['password'],
                host=credentials['server'],
                port=int(credentials['port']),
                database=credentials['database']
            )
            Log('Connected to CIP', 'noprint')
        except mariadb.Error as e:
            Log('Could not connect to CIP on mariadb server', 'noprint')
            exit()

        self.cursor = self.cnxn.cursor()



    def close(self):

        self.cnxn.close()


    def makeTables(self):
        self.cursor.execute(createTables['brands'])
        self.cursor.execute(createTables['articles'])
        self.cursor.execute(createTables['barcodes'])
        self.cursor.execute(createTables['soldout'])
        self.cursor.execute(createTables['imports'])
        self.cursor.execute(createTables['placement'])
        self.cursor.execute(createTables['turnover_hourly'])
        self.cursor.execute(createTables['turnover_daily'])
        self.cnxn.commit()
        Log('All tables created successfully', 'noprint')




    def brandsGetMax(self):
        self.cursor.execute(
            'SELECT MAX(brand_id) FROM brands;')
        result = self.cursor.fetchone()
        if result[0] == None:
            return 0
        else:
            return result[0]


    def articlesGetMax(self):
        self.cursor.execute(
                'SELECT MAX(article_id) FROM articles;')
        result = self.cursor.fetchone()
        if result[0] == None:
            return 0
        else:
            return result[0]


    def brandsPost(self,records: tuple):
        self.cursor.executemany(insertTables['brands'],records)
        self.cnxn.commit()
        Log('Updated table brands')



    def articlesPost(self,records: tuple):
        query = '''
        INSERT INTO articles(article_id, brand_id, art_name)
        VALUES((?), (?), (?));
        '''
        self.cursor.executemany(insertTables['articles'],records)
        self.cnxn.commit()
        Log('Updated table articles')

    def barcodesPost(self,records: list):
        pass




    def soldoutPost(self,records):
        self.cursor.executemany(insertTables['soldout'],records)
        self.cnxn.commit()
        Log('Updated table soldout')


    def importsPost(self,records: list):
        self.cursor.executemany(insertTables['imports'],records)
        self.cnxn.commit()
        Log('Updated table imports')


    def turnover_hourlyPost(self,record: list):
        self.cursor.execute(insertTables['turnover_hourly'],record)
        self.cnxn.commit()
        Log('Updated table turnover_hourly')


    def turnover_dailyPost(self,record: list):
        self.cursor.execute(insertTables['turnover_daily'],record)
        self.cnxn.commit()
        Log('Updated table turnover_daily')


    def storagePost(self,records: list):
        pass


if __name__ == '__main__':
    # run this file to create tables
    c = Postconnect()
    c.makeTables()
    c.close()
