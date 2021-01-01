import mariadb
import sys
from writelog import Log
from postqueries import *


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
            Log(f'Postconnect: Connected to {credentials["database"]}')
        except mariadb.Error:
            Log(f'Postconnect: Could not connect to {credentials["database"]}')
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
        Log('Postconnect: All tables created or exists')


    def brandsGetMax(self):
        self.cursor.execute(
            'SELECT MAX(brand_id) FROM brands;')
        result = self.cursor.fetchone()
        Log('Postconnect: Fetching from brandsGetMax')
        if result[0] == None:
            return 0
        else:
            return result[0]


    def articlesGetMax(self):
        self.cursor.execute(
                'SELECT MAX(article_id) FROM articles;')
        result = self.cursor.fetchone()
        Log('Postconnect: Fetching from articlesGetMax')
        if result[0] == None:
            return 0
        else:
            return result[0]


    def brandsPost(self,records):
        self.cursor.executemany(insertRows['brands'],records)
        self.cnxn.commit()
        Log('Postconnect: Updated table brands')



    def articlesPost(self,records):
        self.cursor.executemany(insertRows['articles'],records)
        self.cnxn.commit()
        Log('Postconnect: Updated table articles')

    def barcodesPost(self,records: list):
        self.cursor.executemany(insertRows['barcodes'],records)
        self.cnxn.commit()
        Log('Postconnect: Updated table barcodes')



    def barcodesDel(self):
        self.cursor.execute(deleteRows['barcodes'])
        self.cnxn.commit()
        Log('Postconnect: Deleted all from table barcodes')


    def soldoutPost(self,records):
        if records == []:
            Log('Postconnect: No sodlouts today, skipping soldout')
        else:
            self.cursor.executemany(insertRows['soldout'],records)
            self.cnxn.commit()
            Log('Postconnect: Updated table soldout')


    def importsPost(self,records):
        if records == []:
            Log('Postconnect: No imports today, skipping imports')
        else:
            self.cursor.executemany(insertRows['imports'],records)
            self.cnxn.commit()
            Log('Postconnect: Updated table imports')


    def turnover_hourlyPost(self,record):
        self.cursor.execute(insertRows['turnover_hourly'],record)
        self.cnxn.commit()
        Log('Postconnect: Updated table turnover_hourly')


    def turnover_dailyPost(self,record):
        self.cursor.execute(insertRows['turnover_daily'],record)
        self.cnxn.commit()
        Log('Postconnect: Updated table turnover_daily')


    def storagePost(self,records):
        pass


if __name__ == '__main__':
    # run this file to create tables
    c = Postconnect()
    c.makeTables()
    c.close()
