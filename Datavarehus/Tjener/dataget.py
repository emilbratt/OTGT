import pyodbc
from writelog import Log


columnNames = {
'clockHoursWeekly':[
'Ukedag','Totalt','00-01','01-02','02-03','03-04','04-05',
'05-06','06-07','07-08','08-09','09-10','10-11','11-12',
'12-13','13-14','14-15','15-16','16-17','17-18','18-19',
'19-20','20-21','21-22','22-23','23-24'
],
'clockHoursMonthly':[
'Dato','Totalt','00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08',
'08-09','09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17',
'17-18','18-19','19-20','20-21','21-22','22-23','23-24'
],
'soldout':[
'Artikkel ID','Merke','Navn','Antall Lager',
'Lagerplass','Sist Importert','Lev. ID'
],
'imports':[
'Artikkel ID','Merke','Navn','Importert','Antall Lager','Lagerplass','Lev.ID'
]
}

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

        # try:
        if 'windows' in driver:
            try:
                Log('Getconnect: Platform: Windows')
                self.cnxn = pyodbc.connect('DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                    driver['windows'], credentials['server'],
                    credentials['database'], credentials['user'],
                    credentials['password']
                    )
                )
                Log(f'Getconnect: Connected to {credentials["database"]}')
            except pyodbc.ProgrammingError:
                Log(f'Getconnect: Could not connect to {credentials["database"]}')
                exit()
        elif 'linux' in driver:
            Log('Getconnect: Platform: Linux')
            try:
                self.cnxn = pyodbc.connect(
                    'DRIVER={FreeTDS};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                    credentials['server'], credentials['port'],
                    credentials['database'], credentials['user'],
                    credentials['password']
                    )
                )
                Log(f'Getconnect: Connected to {credentials["database"]}')
            except pyodbc.ProgrammingError:
                Log(f'Getconnect: Could not connect to {credentials["database"]}')
                exit()

        Log(f'Getconnect: Connected to {credentials["database"]}')

        self.timeGet = 'SELECT CONVERT(VARCHAR(16),GETDATE(),20)'
        self.timestampGet = 'SELECT CONVERT(VARCHAR(20),CURRENT_TIMESTAMP,20)'
        self.YYYYMMDDGET = '''SELECT CONVERT(VARCHAR(10),DATEADD(DAY, (?),CURRENT_TIMESTAMP),112)'''
        self.weekNumGet = '''SELECT DATENAME(WEEK, DATEADD(DAY, (?), CURRENT_TIMESTAMP))'''
        self.dateMonthGet = '''SELECT DATENAME(DAY, DATEADD(DAY, (?), CURRENT_TIMESTAMP))'''
        self.weekdayGet = '''SELECT DATENAME(WEEKDAY, DATEADD(DAY, (?), CURRENT_TIMESTAMP))'''
        self.monthGet = '''SELECT DATENAME(MONTH, DATEADD(DAY, (?), CURRENT_TIMESTAMP))'''

        self.yesterday = -1 # subtract 1 day from todays date
        # self.days = [-1,-8,-15] # getting from last day, same weekday the week before and the week before that

        self.cursor = self.cnxn.cursor()

        self.cursor.execute('SET LANGUAGE NORWEGIAN')

        self.time = self.cursor.execute(self.timeGet).fetchone()[0][11:16]

        self.timestamp = self.cursor.execute(self.timestampGet).fetchone()[0]

        self.YYYYMMDD = self.cursor.execute(self.YYYYMMDDGET,0).fetchone()[0]

        self.weekNum = self.cursor.execute(self.weekNumGet,0).fetchone()[0]

        self.weekday = self.cursor.execute(self.weekdayGet,0).fetchone()[0]

        self.weekdayYesterday = self.cursor.execute(
            self.weekdayGet,self.yesterday).fetchone()[0]

        self.yesterdayYYYMMDD = self.cursor.execute(
            self.YYYYMMDDGET,self.yesterday).fetchone()[0]

        self.weekNumYesterday = self.cursor.execute(
            self.weekNumGet,self.yesterday).fetchone()[0]

        self.monthYesterday = self.cursor.execute(
            self.monthGet,self.yesterday).fetchone()[0]

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
        data['yesterday']['month'] = self.monthYesterday
        data['yesterday']['human'] = self.dateYesterdayHuman
        data['yesterday']['YYYY-weekNum'] = self.yesterdayYYYMMDD[
            :4]+'-'+self.weekNumYesterday
        data['weekly'] = self.cursor.execute(
            'SELECT DATEPART(WEEKDAY, CURRENT_TIMESTAMP)').fetchone()[0] == 1
        data['monthly'] = self.cursor.execute(
            'SELECT DATEPART(DAY, CURRENT_TIMESTAMP)').fetchone()[0] == 1
        Log('Getconnect: Fetching from fetchTime')
        return data


    def getBrands(self,val):
        result = self.cursor.execute('''
        SELECT
            brandId, brandLabel
        FROM
            Brands
        WHERE
            brandId > (?)
        ORDER BY
            brandId
        ''', val).fetchall()
        Log('Getconnect: Fetching from getBrands')
        return result


    def getArticles(self,val):
        result = self.cursor.execute('''
        SELECT
            articleId, brandId, articleName
        FROM
            Article
        WHERE
            articleId > (?)
        ORDER BY
            articleId
        ''',val).fetchall()
        Log('Getconnect: Fetching from getArticles')
        return result


    def getBarcodes(self):
        result = self.cursor.execute('''
        SELECT
            articleId, eanCode
        FROM
            ArticleEAN
        ''').fetchall()
        Log('Getconnect: Fetching from getBarcodes')
        return result

    def turnoverDaily(self):
        result = []
        rows = []
        total = self.cursor.execute('''
            SELECT
            	CASE
            		WHEN CAST(SUM(Brto_Salg_Kr) AS INT) IS NULL THEN 0
            		ELSE CAST(SUM(Brto_Salg_Kr) AS INT)
            	END
            FROM
                view_HIP_salesInfo_10
            WHERE
                DATEPART(DAYOFYEAR, [salesdate]) = DATEPART(DAYOFYEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                DATEPART(YEAR, [salesdate]) = DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                isGiftCard ='0'
        ''',self.yesterday,self.yesterday).fetchone()

        rows.append(total[0])

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
        for hour in range(24): # append each hours turnover for each hour of the day
            hourly = self.cursor.execute(query,hour,self.yesterday,self.yesterday).fetchone()
            rows.append(hourly[0])

        Log('Getconnect: Fetching from turnoverDaily')
        result.append(rows)
        return result


    def turnoverWeekly(self):
        data = []
        rowSum = [0] * 25 # adding values while iterating
        rowSum.insert(0, 'SUM')

        data.append(['Omsetning'])
        data.append([
            'Uke-'+str(self.weekNumYesterday) + ' ' +
            str(self.yesterdayYYYMMDD[:4])])

        data.append(columnNames['clockHoursWeekly'])
        for i in range(-7,0,1):
            record = []
            record.append(self.cursor.execute(
                self.weekdayGet,i).fetchone()[0])

            total = self.cursor.execute('''
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
            ''',i,self.yesterday,self.yesterday).fetchone()

            record.append(total[0])

            for hour in range(24): # append each hours turnover for each hour of the day
                hourly = self.cursor.execute( '''
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

                ''',hour,i,self.yesterday).fetchone()
                record.append(hourly[0])

            # after appending values, calculate sum for last row
            for i in range(len(record)):
                if i != 0:
                    rowSum[i] += record[i]

            data.append(record)

        data.append(rowSum)
        Log('Getconnect: Fetching from turnoverWeekly')
        return data


    def turnoverMonthly(self):
        data = []
        rowSum = [0] * 25 # adding values while iterating
        rowSum.insert(0, 'SUM')

        data.append(['Omsetning'])
        data.append([
            self.monthYesterday.title() + ' ' + self.yesterdayYYYMMDD[:4]])

        data.append(columnNames['clockHoursMonthly'])

        daysTotal = self.cursor.execute(
        'SELECT DAY(DATEADD(DD,-1,DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0)))'
        ).fetchone()[0]

        for i in range((-daysTotal),0,1):
            record = []
            record.append(i+daysTotal+1)

            total = self.cursor.execute('''
                SELECT
                	CASE
                		WHEN CAST(SUM(Brto_Salg_Kr) AS INT) IS NULL THEN 0
                		ELSE CAST(SUM(Brto_Salg_Kr) AS INT)
                	END
                FROM
                    view_HIP_salesInfo_10
                WHERE
                    DATEPART(DAYOFYEAR, [salesdate]) = DATEPART(DAYOFYEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                    DATEPART(YEAR, [salesdate]) = DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
                    isGiftCard ='0'
            ''',i,self.yesterday,).fetchone()

            record.append(total[0])

            for hour in range(24): # append each hours turnover for each hour of the day
                hourly = self.cursor.execute( '''
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

                ''',hour,i,self.yesterday).fetchone()
                record.append(hourly[0])

            # after appending values, calculate sum for last row
            for i in range(len(record)):
                if i != 0:
                    rowSum[i] += record[i]

            data.append(record)

        Log('Getconnect: Fetching from turnoverMonthly')
        data.append(rowSum)
        return data


    def soldoutDaily(self):
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

        Log('Getconnect: Fetching from soldoutDaily')
        return data


    def soldoutWeekly(self):
        data = []

        data.append(['Utsolgt'])
        data.append([
            'Uke-'+str(self.weekNumYesterday) + ' ' +
            str(self.yesterdayYYYMMDD[:4])])

        data.append(['Utsolgte Varer'])
        data.append(columnNames['soldout'])

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
        ''',self.yesterday,self.yesterday).fetchall()

        for row in result:
            data.append(row)

        Log('Getconnect: Fetching from soldoutWeekly')
        return data


    def soldoutMonthly(self):
        data = []

        data.append(['Utsolgt'])
        data.append([
            self.monthYesterday.title() + ' ' + self.yesterdayYYYMMDD[:4]])

        data.append(['Utsolgte Varer'])
        data.append(columnNames['soldout'])

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
        	DATEPART(MONTH, articleStock.lastSold) =  DATEPART(MONTH, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
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
        ''',self.yesterday,self.yesterday).fetchall()

        for row in result:
            data.append(row)

        Log('Getconnect: Fetching from soldoutMonthly')
        return data


    def importsDaily(self):

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
        Log('Getconnect: Fetching from importsDaily')
        return data


    def importsWeekly(self):
        data = []

        data.append(['Vareimport'])
        data.append([
            'Uke-'+str(self.weekNumYesterday) + ' ' +
            str(self.yesterdayYYYMMDD[:4])])

        data.append(columnNames['imports'])

        articleList = self.cursor.execute('''
        SELECT
        	articleId,
        	stockAdjustmenId
        FROM
        	StockAdjustment
        WHERE
        	DATEPART(WEEK, [adjustmentDate]) = DATEPART(WEEK, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
            adjustmentCode ='41'
        ORDER BY
        	adjustmentDate
        ''',self.yesterday,self.yesterday).fetchall()

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
        Log('Getconnect: Fetching from importsWeekly')
        return data


    def importsMonthly(self):
        data = []

        data.append(['Vareimport'])
        data.append([
            self.monthYesterday.title() + ' ' + self.yesterdayYYYMMDD[:4]])

        data.append(columnNames['imports'])

        articleList = self.cursor.execute('''
        SELECT
        	articleId,
        	stockAdjustmenId
        FROM
        	StockAdjustment
        WHERE
        	DATEPART(MONTH, [adjustmentDate]) = DATEPART(MONTH, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
        	DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, DATEADD(DAY, (?), CURRENT_TIMESTAMP)) AND
            adjustmentCode ='41'
        ORDER BY
        	adjustmentDate
        ''',self.yesterday,self.yesterday).fetchall()

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
        Log('Getconnect: Fetching from importsMonthly')
        return data

if __name__ == '__main__':
    pass
