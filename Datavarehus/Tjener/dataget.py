import pyodbc
from writelog import Log


def loadDriver():
    import os, sys
    if sys.platform.startswith('linux'):
        return {'linux':'FreeTDS'}
    elif sys.platform.startswith('win32'):
        return {'windows':'ODBC Driver 17 for SQL Server'}
    elif sys.platform.startswith('darwin'):
        # dont support mac, yet
        return False
    else:
        return False

def humanYYYYMMDD(YYYYMMDD):
    year = YYYYMMDD[:4]
    month = YYYYMMDD[4:6]
    day = YYYYMMDD[6:8]
    return f'{day}-{month}-{year}'



def transferDatawarehouse(records):
    '''
        this function sends the results from the queries
        and sends the data to the data-warehouse
    '''
    pass


class Getconnect:
    def __init__(self):
        from credentials import loadCredentials
        credentials = loadCredentials('get')
        driver = loadDriver()

        if 'windows' in driver:
            Log('Platform: Windows','noprint')
            self.cnxn = pyodbc.connect('DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                driver['windows'], credentials['server'],
                credentials['database'], credentials['user'],
                credentials['password']
                )
            )
        elif 'linux' in driver:
            Log('Platform: Linux','noprint')
            self.cnxn = pyodbc.connect(
                'DRIVER={FreeTDS};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                credentials['server'], credentials['port'],
                credentials['database'], credentials['user'],
                credentials['password']
                )
            )

        self.yesterday = -1 # subtract 1 day from todays date
        self.days = [-1,-8,-15] # getting from last day, same weekday the week before and the week before that

        self.cursor = self.cnxn.cursor()
        self.cursor.execute('SET LANGUAGE NORWEGIAN')

        self.YYYYMMDD = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(10),CURRENT_TIMESTAMP,112)').fetchone()[0]

        self.weekNum = self.cursor.execute(
            'SELECT DATENAME(WEEK, CURRENT_TIMESTAMP)').fetchone()[0]

        self.weekday = self.cursor.execute(
            'SELECT DATENAME(WEEKDAY, CURRENT_TIMESTAMP)').fetchone()[0]
        self.timestamp = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(20),CURRENT_TIMESTAMP,20)').fetchone()[0]
        self.time = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(16),GETDATE(),20)').fetchone()[0][11:16]

        self.weekdayYesterday = self.cursor.execute(
            'SELECT DATENAME(WEEKDAY, DATEADD(DAY, (?), CURRENT_TIMESTAMP))'
            ,self.yesterday).fetchone()[0]

        self.yesterdayYYYMMDD = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(10),DATEADD(DAY, -1,CURRENT_TIMESTAMP),112)'
            ).fetchone()[0]

        self.weekNumYesterday = self.cursor.execute('''
            SELECT DATENAME(WEEK, DATEADD(DAY, -1, CURRENT_TIMESTAMP))
            ''').fetchone()[0]

        self.dateHuman = humanYYYYMMDD(self.YYYYMMDD)
        self.dateYesterdayHuman = humanYYYYMMDD(self.yesterdayYYYMMDD)


    def close(self):
        self.cursor.close()
        self.cnxn.close()


    def fetchTime(self):
        data = {}
        data['today'] = {}
        data['yesterday'] = {}

        data['today']['time'] = self.time
        data['today']['timestamp'] = self.timestamp
        data['today']['YYYYMMDD'] = self.YYYYMMDD
        data['today']['weekNum'] = self.weekNum
        data['today']['weekday'] = self.weekday
        data['today']['human'] = self.dateHuman
        data['yesterday']['YYYYMMDD'] = self.yesterdayYYYMMDD
        data['yesterday']['weekNum'] = self.weekNumYesterday
        data['yesterday']['weekday'] = self.weekdayYesterday
        data['yesterday']['human'] = self.dateYesterdayHuman
        return data



    def importsYesterdayy(self):

        articleList = self.cursor.execute('''
        SELECT
        	articleId,
        	stockAdjustmenId
        FROM
        	StockAdjustment
        WHERE
            DATEPART(WEEKDAY, [adjustmentDate]) = DATEPART(WEEKDAY, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(WEEK, [adjustmentDate]) = DATEPART(WEEK, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
            adjustmentCode ='41'
        ORDER BY
        	adjustmentDate
        ''',self.yesterday,self.yesterday,self.yesterday).fetchall()

        data = []
        for article in articleList:
            for importInfo in self.cursor.execute('''
                SELECT
                    Article.articleId,
                    Brands.brandLabel AS Merke,
                    Article.articleName AS Navn,
                    CAST(StockAdjustment.adjustmentQty AS INT) AS Antall_Importert,
                    CAST (stockQty AS INT) AS Antall_Lager,
                    articleStock.StorageShelf AS Lager_plass,
                    Article.suppliers_art_no AS LeverandorID

                FROM
                    Article
                    INNER JOIN articleStock ON Article.articleId = articleStock.articleId
                    INNER JOIN Brands ON Article.brandId = Brands.brandId
                    INNER JOIN StockAdjustment ON Article.articleId = StockAdjustment.articleId

                WHERE
                    Article.articleId =(?) AND adjustmentCode ='41' AND stockAdjustmenId = (?)
                ''', article[0], article[1]).fetchall():
                data.append(importInfo)

        return data



    def getArticles(self,val):
        return self.cursor.execute('''
        SELECT
            articleId, brandId, articleName
        FROM
            Article
        WHERE
            articleId > (?)
        ORDER BY
            articleId
        ''',val).fetchall()


    def getBrands(self,val):
        return self.cursor.execute('''
        SELECT
            brandId, brandLabel
        FROM
            Brands
        WHERE
            brandId > (?)
        ORDER BY
            brandId
        ''', val).fetchall()

    def turnoverYesterday(self):
        data = []
        total = self.cursor.execute('''
            SET
                LANGUAGE NORWEGIAN
            SELECT
            	CASE
            		WHEN CAST(SUM(Brto_Salg_Kr) AS INT) IS NULL THEN 0
            		ELSE CAST(SUM(Brto_Salg_Kr) AS INT)
            	END
            FROM
                view_HIP_salesInfo_10
            WHERE
                DATEPART(WEEKDAY,[salesdate]) = DATEPART(WEEKDAY,DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                DATEPART(WEEK, [salesdate]) = DATEPART(WEEK, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                DATEPART(YEAR, [salesdate]) = DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                isGiftCard ='0'
        ''',self.yesterday,self.yesterday,self.yesterday).fetchone()

        data.append(total[0])

        query = '''
            SELECT
            	CASE
            		WHEN CAST(SUM(Brto_Salg_Kr) AS INT) IS NULL THEN 0
            		ELSE CAST(SUM(Brto_Salg_Kr) AS INT)
            	END
            FROM
                view_HIP_salesInfo_10
            WHERE
                DATEPART(HOUR, [salesdate]) = (?) AND
                DATEPART(DAYOFYEAR, [salesdate]) = DATEPART(DAYOFYEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                DATEPART(YEAR, [salesdate]) = DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                isGiftCard = '0'

        '''
        for hour in range(24): # append each horus turnover for each hour of the day
            hourly = self.cursor.execute(query,hour,self.yesterday,self.yesterday).fetchone()
            data.append(hourly[0])


        return [data]

    def soldoutYesterdayy(self):
        data = []

        result = self.cursor.execute('''
        SELECT
            Article.articleId,
            Brands.brandLabel AS Merke,
            Article.articleName AS Navn,
            CAST (stockQty AS INT) AS Antall_Lager,
            articleStock.StorageShelf AS Lager,
            CONVERT(VARCHAR(10), articleStock.lastReceivedFromSupplier, 105) AS Siste_Importdato,
            Article.suppliers_art_no AS Leverandor
        FROM
            ((Article
            INNER JOIN articleStock ON Article.articleId = articleStock.articleId)
            INNER JOIN Brands ON Article.brandId = Brands.brandId)
        WHERE
        	DATEPART(WEEKDAY, articleStock.lastSold) =  DATEPART(WEEKDAY, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(WEEK, articleStock.lastSold) =  DATEPART(WEEK, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(YEAR, articleStock.lastSold) =  DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
        	ArticleStatus = '0' AND Article.articleName NOT LIKE '[.]%' AND stockQty<='0' AND
        	[articleName] NOT LIKE '%REPOSE DESIGNFOREVIG%' AND
        	[articleName] NOT LIKE 'Retain 24 gavekort%' AND
        	[articleName] NOT LIKE 'Diverse Vinding%' AND
        	[articleName] NOT LIKE 'Diverse Glass%' AND
        	[articleName] NOT LIKE 'MARIMEKKO LUNSJSERVIETTER%' AND
        	[articleName] NOT LIKE 'Diverse SERVISE%' AND
        	[articleName] NOT LIKE 'IHR LUNSJSERVIETTER%'
        ORDER BY
        	brandLabel
        ''', self.yesterday,self.yesterday,self.yesterday).fetchall()

        for row in result:
            data.append(row)

        return data


if __name__ == '__main__':
    print('ok')
