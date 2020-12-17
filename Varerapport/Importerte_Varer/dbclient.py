import pyodbc
from logging import Log


class connect:
    def __init__(self):
        from credentials import loadCredentials
        from driver import loadDriver

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
        self.cursor.execute('SET LANGUAGE NORWEGIAN')
        self.YYYYMMDD = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(10),CURRENT_TIMESTAMP,112)').fetchone()[0]
        self.weekNum = self.cursor.execute(
            'SELECT DATENAME(WEEK, CURRENT_TIMESTAMP)-1').fetchone()[0]
        self.weekday = self.cursor.execute(
            'SELECT DATENAME(WEEKDAY, CURRENT_TIMESTAMP)').fetchone()[0]
        self.timestamp = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(20),CURRENT_TIMESTAMP,20)').fetchone()[0]
        self.time = self.cursor.execute(
            'SELECT CONVERT(VARCHAR(16),GETDATE(),20)').fetchone()[0]


    def getToday(self):
        fetchList = '''
        SELECT articleId,
        stockAdjustmenId
        FROM StockAdjustment
        WHERE
        adjustmentDate >= DATEADD(day, DATEDIFF(day, 0, GETDATE()), 0) AND
        adjustmentCode ='41'
        ORDER BY adjustmentDate
        '''
        fethInfo = '''
        SELECT
        Article.suppliers_art_no AS LeverandorID,
        Brands.brandLabel AS Merke,
        Article.articleName AS Navn,
        CAST(StockAdjustment.adjustmentQty AS INT) AS Antall_Importert,
        CAST (stockQty AS INT) AS Antall_Lager,
        articleStock.StorageShelf AS Lager_plass
        FROM Article
        INNER JOIN articleStock ON Article.articleId = articleStock.articleId
        INNER JOIN Brands ON Article.brandId = Brands.brandId
        INNER JOIN StockAdjustment ON Article.articleId = StockAdjustment.articleId
        WHERE
        Article.articleId =(?) AND adjustmentCode ='41' AND stockAdjustmenId = (?)
        '''
        result = self.cursor.execute(fetchList).fetchall()
        data = []

        # data.append(title)
        for article in result:
            for importInfo in self.cursor.execute(fethInfo, article[0], article[1]).fetchall():

                data.append(importInfo)

        title = [
        'Lev.ID','Merke','Navn',
        'Ant.Importert','Ant.Lager','Plassering'
        ]
        data.insert(0,title)
        return data

# SELECT CAST(columnname AS INT) AS columnname from tablename

    def close(self):
        self.cursor.close()
        self.cnxn.close()
