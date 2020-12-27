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

class connect:
    def __init__(self):
        from credentials import loadCredentials
        credentials = loadCredentials()
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

        self.cursor = self.cnxn.cursor()
        self.YYYYMMDD = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(10),CURRENT_TIMESTAMP,112)').fetchone()[0]
        self.yesterdayYYYMMDD = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(10),DATEADD(day, -1,CURRENT_TIMESTAMP),112)'
            ).fetchone()[0]
        self.weekNum = self.cursor.execute(
            'SELECT DATENAME(WEEK, CURRENT_TIMESTAMP)-1').fetchone()[0]
        self.weekday = self.cursor.execute(
            'SELECT DATENAME(WEEKDAY, CURRENT_TIMESTAMP)').fetchone()[0]
        self.timestamp = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(20),CURRENT_TIMESTAMP,20)').fetchone()[0]
        self.time = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(16),GETDATE(),20)').fetchone()[0]
        self.day = -1 # subtract days from todays date
        self.days = [-1,-8,-15] # getting from last day, same weekday the week before and the week before that

    def close(self):
        self.cursor.close()
        self.cnxn.close()


    def imports(self):

        articleList = self.cursor.execute('''
        SELECT
        	articleId,
        	stockAdjustmenId
        FROM
        	StockAdjustment
        WHERE
            DATEPART(WEEKDAY, [adjustmentDate]) >= DATEPART(WEEKDAY, DATEADD(day, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(WEEK, [adjustmentDate]) >= DATEPART(WEEK, DATEADD(day, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(YEAR, [adjustmentDate]) >= DATEPART(YEAR, DATEADD(day, (?), CURRENT_TIMESTAMP)) AND
            adjustmentCode ='41'
        ORDER BY
        	adjustmentDate
        ''',self.day,self.day,self.day).fetchall()

        fethData = '''
        SELECT
            Article.suppliers_art_no AS LeverandorID,
            Brands.brandLabel AS Merke,
            Article.articleName AS Navn,
            CAST(StockAdjustment.adjustmentQty AS INT) AS Antall_Importert,
            CAST (stockQty AS INT) AS Antall_Lager,
            articleStock.StorageShelf AS Lager_plass

        FROM
            Article
            INNER JOIN articleStock ON Article.articleId = articleStock.articleId
            INNER JOIN Brands ON Article.brandId = Brands.brandId
            INNER JOIN StockAdjustment ON Article.articleId = StockAdjustment.articleId

        WHERE
            Article.articleId =(?) AND adjustmentCode ='41' AND stockAdjustmenId = (?)
        '''

        data = []

        for article in articleList:
            for importInfo in self.cursor.execute('''
                SELECT
                    Article.suppliers_art_no AS LeverandorID,
                    Brands.brandLabel AS Merke,
                    Article.articleName AS Navn,
                    CAST(StockAdjustment.adjustmentQty AS INT) AS Antall_Importert,
                    CAST (stockQty AS INT) AS Antall_Lager,
                    articleStock.StorageShelf AS Lager_plass

                FROM
                    Article
                    INNER JOIN articleStock ON Article.articleId = articleStock.articleId
                    INNER JOIN Brands ON Article.brandId = Brands.brandId
                    INNER JOIN StockAdjustment ON Article.articleId = StockAdjustment.articleId

                WHERE
                    Article.articleId =(?) AND adjustmentCode ='41' AND stockAdjustmenId = (?)
                ''', article[0], article[1]).fetchall():
                data.append(importInfo)

        title = [
        'Lev.ID','Merke','Navn',
        'Importert','Lager','Plass'
        ]

        data.insert(0,title)
        return data




    def sales(self):

        data = []
        for day in self.days:
            tempList = []
            tempList.append(self.cursor.execute('''
            SET
                LANGUAGE NORWEGIAN
            SELECT
                DATENAME(WEEKDAY, DATEADD(day, (?), CURRENT_TIMESTAMP))
            ''',day).fetchone())

            tempList.append(self.cursor.execute('''
                SET
                    LANGUAGE NORWEGIAN
                SELECT
                    REPLACE(CAST(SUM(Brto_Salg_Kr) AS DECIMAL(29,2)) ,'.',',')
                FROM
                    view_HIP_salesInfo_10
                WHERE
                    DATEPART(WEEKDAY,[salesdate]) = DATEPART(WEEKDAY,DATEADD(day, (?), CURRENT_TIMESTAMP)) AND
                    DATEPART(WEEK, [salesdate]) = DATEPART(WEEK, DATEADD(day, (?), CURRENT_TIMESTAMP)) AND
                    DATEPART(YEAR, [salesdate]) = DATEPART(YEAR, DATEADD(day, (?), CURRENT_TIMESTAMP)) AND
                    isGiftCard ='0'
            ''',day,day,day).fetchone())

            data.append(tempList)

        return data


























    def importss(self):
        fetchList = '''
        SELECT
            articleId,
            stockAdjustmenId
        FROM
            StockAdjustment
        WHERE
            adjustmentDate >= DATEADD(day, DATEDIFF(day, 0, GETDATE()), 0) AND
            adjustmentCode ='41'
        ORDER BY
            adjustmentDate
        '''
        fethInfo = '''
        SELECT
            Article.suppliers_art_no AS LeverandorID,
            Brands.brandLabel AS Merke,
            Article.articleName AS Navn,
            CAST(StockAdjustment.adjustmentQty AS INT) AS Antall_Importert,
            CAST (stockQty AS INT) AS Antall_Lager,
            articleStock.StorageShelf AS Lager_plass

        FROM
            Article
            INNER JOIN articleStock ON Article.articleId = articleStock.articleId
            INNER JOIN Brands ON Article.brandId = Brands.brandId
            INNER JOIN StockAdjustment ON Article.articleId = StockAdjustment.articleId

        WHERE
            Article.articleId =(?) AND adjustmentCode ='41' AND stockAdjustmenId = (?)
        '''
        result = self.cursor.execute(fetchList).fetchall()
        data = []

        for article in result:
            for importInfo in self.cursor.execute(fethInfo, article[0], article[1]).fetchall():
                data.append(importInfo)

        title = [
        'Lev.ID','Merke','Navn',
        'Importert','Lager','Plass'
        ]

        data.insert(0,title)
        return data
