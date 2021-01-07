import pyodbc
from writelog import Log


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


    def getYYYYMMDD(self, days):
        query = '''
        SELECT CONVERT(VARCHAR(10),DATEADD(DAY, -(?), CURRENT_TIMESTAMP),112)
        '''
        return self.cursor.execute(query,days).fetchone()[0]


    def getImport(self,days):
        fetchList = '''
        SELECT
            articleId,
            stockAdjustmenId
        FROM
            StockAdjustment
        WHERE
        	DATEPART(DAY, [adjustmentDate]) = DATEPART(DAY, DATEADD(DAY, -(?), CURRENT_TIMESTAMP)) AND
        	DATEPART(YEAR, [adjustmentDate]) = DATEPART(YEAR, DATEADD(DAY, -(?), CURRENT_TIMESTAMP)) AND
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
        result = self.cursor.execute(fetchList,days,days).fetchall()
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


    def showSingleItemInfo(self,barcode):
        query = '''
        SELECT
            Brands.brandLabel,
            Article.articleName,
            CAST (articleStock.stockQty AS INT),
            articleStock.StorageShelf,
            articleStock.lastSold,
            articleStock.lastReceivedFromSupplier,
            Article.brandId,
            ArticleEAN.eanCode

        FROM
            (((Article
            FULL JOIN articleStock ON Article.articleId = articleStock.articleId)
            FULL JOIN ArticleEAN ON Article.articleId = ArticleEAN.articleId)
            FULL JOIN Brands ON Article.brandId = Brands.brandId)

        WHERE
            ArticleEAN.eanCode=(?)
        '''
        result = self.cursor.execute(query,barcode).fetchall()
        data = []


        title = [
        'Merke','Navn','Antall','Lagerplass',
        'Sist Solgt','Sist Importert','Lev. ID','Strekkode'
        ]
        data.append(title)
        for row in result:
            data.append(row)

        return data

    def showSingleItemExtendedInfo(self, barcode):
        query = '''
        SELECT
        	Merke,
        	Navn,
        	Kategori,
        	CAST (Pris AS INT),
            CAST (Antall_lager AS INT),
        	Lagerplass,
        	Leverandor_nummer,
            Sist_lagt_inn_dato,
            Sist_solgt_dato,


        	CASE
        		WHEN Antall_solgt_siste_730 IS NULL THEN 0
        		ELSE Antall_solgt_siste_730
        	END AS Antall_solgt_siste_730,

        	CASE
        		WHEN Antall_solgt_siste_365 IS NULL THEN 0
        		ELSE Antall_solgt_siste_365
        	END AS Antall_solgt_siste_365,

        	CASE
        		WHEN Antall_solgt_siste_180 IS NULL THEN 0
        		ELSE Antall_solgt_siste_180
        	END AS Antall_solgt_siste_180,


        	CASE
        		WHEN Antall_solgt_siste_30 IS NULL THEN 0
        		ELSE Antall_solgt_siste_30
        	END AS Antall_solgt_siste_30
        FROM
        	Article
        INNER JOIN
        	ArticleEAN ON Article.articleId = ArticleEAN.articleId
        	/* Henter opp info fra view_HIP_Productinfo*/
        LEFT JOIN
        	(select
        	view_HIP_Productinfo.ArticleId AS aArtId,
        	view_HIP_Productinfo.brandLabel AS Merke,
        	view_HIP_Productinfo.articleName AS Navn,
        	view_HIP_Productinfo.ArticleGroupName AS Kategori,
        	view_HIP_Productinfo.articleUnitPrice AS Pris,
        	view_HIP_Productinfo.supplierId AS Leverandor_id
        	/*,view_HIP_Productinfo.locationName AS lokasjon*/
        FROM
        	view_HIP_Productinfo)a /* a beskriver egendefinert tabellnavn på tabell-i-tabell*/
        		on a.aArtId = Article.ArticleId/* slår sammen artikkelid i a-tabell med article-tabell */
        	/*Henter opp info fra articlestock*/
        LEFT JOIN(
        	SELECT
        		Article.ArticleId as bArtId,
        		articleStock.stockQty AS Antall_Lager,
        		articleStock.StorageShelf AS Lagerplass,
        		Article.suppliers_art_no AS Leverandor_nummer,
        		articleStock.lastReceivedFromSupplier AS Sist_lagt_inn_dato,
        		articleStock.lastSold AS Sist_solgt_dato
        	FROM
        			((Article
        		INNER JOIN
        			articleStock ON Article.articleId = articleStock.articleId)
        		INNER JOIN
        			Brands ON Article.brandId = Brands.brandId)
        		)b on b.bArtId = Article.ArticleId/* b beskriver egendefinert tabellnavn på tabell-i-tabell*/
        		/*Henter opp info om antall solgt siste 365 dager*/
        LEFT JOIN(
        	SELECT
        		Article.ArticleId as cArtId,
        		CAST (SUM(adjustmentQty) AS INT) as Antall_solgt_siste_365
        	FROM
        		Article
        	INNER JOIN
        		StockAdjustment ON Article.articleId = StockAdjustment.articleId
        	WHERE
        		adjustmentCode ='9' AND
        		adjustmentDate >= dateadd(dd, -365, getdate())
        	Group by Article.ArticleId
        )c on c.cArtid = Article.ArticleId/* c beskriver egendefinert tabellnavn på tabell-i-tabell*/
        LEFT JOIN(
        	SELECT
        		Article.ArticleId as cArtId,
        		CAST (SUM(adjustmentQty) AS INT) as Antall_solgt_siste_180
        	FROM
        		Article
        	INNER JOIN
        		StockAdjustment ON Article.articleId = StockAdjustment.articleId
        	WHERE
        		adjustmentCode ='9' AND
        		adjustmentDate >= dateadd(dd, -180, getdate())
        	Group by Article.ArticleId
        )d on d.cArtid = Article.ArticleId/* d beskriver egendefinert tabellnavn på tabell-i-tabell*/
        LEFT JOIN(
        	SELECT
        		Article.ArticleId as cArtId,
        		CAST (SUM(adjustmentQty) AS INT) as Antall_solgt_siste_730
        	FROM
        		Article
        	INNER JOIN
        		StockAdjustment ON Article.articleId = StockAdjustment.articleId
        	WHERE
        		adjustmentCode ='9' AND
        		adjustmentDate >= dateadd(dd, -730, getdate())
        	Group by Article.ArticleId
        )e on e.cArtid = Article.ArticleId/* e beskriver egendefinert tabellnavn på tabell-i-tabell*/
        LEFT JOIN(
        	SELECT
        		Article.ArticleId as cArtId,
        		CAST (SUM(adjustmentQty) AS INT) as Antall_solgt_siste_30
        	FROM
        		Article
        	INNER JOIN
        		StockAdjustment ON Article.articleId = StockAdjustment.articleId
        	WHERE
        		adjustmentCode ='9' AND
        		adjustmentDate >= dateadd(dd, -30, getdate())
        	Group by Article.ArticleId
        )f on f.cArtid = Article.ArticleId/* f beskriver egendefinert tabellnavn på tabell-i-tabell*/

        WHERE
        	ArticleEAN.eanCode=(?)
        '''
        result = self.cursor.execute(query,barcode).fetchall()
        data = []


        title = [
        'Merke','Navn','Kategori','Pris',
        'Antall','Plass','Lev. ID','Sist Importert','Sist Solgt og antall solgt siste->',
        '2 år','1 år','Halvår','Måned'
        ]
        data.append(title)
        for row in result:
            data.append(row)

        return data


    def close(self):
        self.cursor.close()
        self.cnxn.close()
