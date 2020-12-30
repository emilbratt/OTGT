createTables = {
'brands':'''
CREATE TABLE IF NOT EXISTS brands(
brand_id    INT UNSIGNED  NOT NULL,
brand_name  VARCHAR(255)  NOT NULL,
PRIMARY KEY (brand_id)
);
''',
'articles':'''
CREATE TABLE IF NOT EXISTS articles(
article_id  INT UNSIGNED  NOT NULL,
brand_id    INT UNSIGNED  NULL,
art_name    VARCHAR(255)  NOT NULL,
PRIMARY KEY (article_id),
FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
);
''',
'barcodes':'''
CREATE TABLE IF NOT EXISTS barcodes(
article_id  INT UNSIGNED  NOT NULL,
barcode     VARCHAR(255)  NOT NULL,
FOREIGN KEY (article_id) REFERENCES articles(article_id)
);
''',
'soldout':'''
CREATE TABLE IF NOT EXISTS soldout(
article_id      INT UNSIGNED    NOT NULL,
brand_name      VARCHAR(255)    NOT NULL,
art_name        VARCHAR(255)    NOT NULL,
stock_qty       INT             NULL,
stock_location  VARCHAR(255)    NULL,
last_import     VARCHAR(255)    NULL,
supply_id       VARCHAR(255)    NOT NULL,
year            INT             NOT NULL,
month           INT             NOT NULL,
date            INT             NOT NULL,
week            INT             NOT NULL,
weekday         VARCHAR(255)    NOT NULL,
yyyymmdd        INT             NOT NULL,
humandate       CHAR(10)        NOT NULL,
FOREIGN KEY (article_id) REFERENCES articles(article_id)
);
''',
'imports':'''
CREATE TABLE IF NOT EXISTS imports(
article_id      INT UNSIGNED    NOT NULL,
brand_name      VARCHAR(255)    NOT NULL,
art_name        VARCHAR(255)    NOT NULL,
stock_qty       INT             NULL,
location        char(10)        NULL,
last_import     VARCHAR(255)    NULL,
year            INT             NOT NULL,
month           INT             NOT NULL,
date            INT             NOT NULL,
week            INT             NOT NULL,
weekday         VARCHAR(255)    NOT NULL,
yyyymmdd        INT             NOT NULL,
humandate       CHAR(10)        NOT NULL,
FOREIGN KEY (article_id) REFERENCES articles(article_id)
);
''',
'placement':'''
CREATE TABLE IF NOT EXISTS placement(
barcode     VARCHAR(255)    NOT NULL,
location    char(10)        NOT NULL,
year        INT             NOT NULL,
month       INT             NOT NULL,
date        INT             NOT NULL,
timestamp   CHAR(30)        NOT NULL,
yyyymmdd    INT             NOT NULL,
humandate   CHAR(10)        NOT NULL
);
''',
'turnover_hourly':'''
CREATE TABLE IF NOT EXISTS turnover_hourly(
`00`        INT         NOT NULL,
`01`        INT         NOT NULL,
`02`        INT         NOT NULL,
`03`        INT         NOT NULL,
`04`        INT         NOT NULL,
`05`        INT         NOT NULL,
`06`        INT         NOT NULL,
`07`        INT         NOT NULL,
`08`        INT         NOT NULL,
`09`        INT         NOT NULL,
`10`        INT         NOT NULL,
`11`        INT         NOT NULL,
`12`        INT         NOT NULL,
`13`        INT         NOT NULL,
`14`        INT         NOT NULL,
`15`        INT         NOT NULL,
`16`        INT         NOT NULL,
`17`        INT         NOT NULL,
`18`        INT         NOT NULL,
`19`        INT         NOT NULL,
`20`        INT         NOT NULL,
`21`        INT         NOT NULL,
`22`        INT         NOT NULL,
`23`        INT         NOT NULL,
year        SMALLINT    NOT NULL,
month       TINYINT     NOT NULL,
date        TINYINT     NOT NULL,
week        TINYINT     NOT NULL,
weekday     CHAR(10)    NOT NULL,
yyyymmdd    INT         NOT NULL,
humandate   CHAR(10)    NOT NULL
);
''',
'turnover_daily':'''
CREATE TABLE IF NOT EXISTS turnover_daily(
sum         INT         NOT NULL,
year        SMALLINT    NOT NULL,
month       TINYINT     NOT NULL,
date        TINYINT     NOT NULL,
week        TINYINT     NOT NULL,
weekday     CHAR(10)    NOT NULL,
yyyymmdd    INT         NOT NULL,
humandate   CHAR(10)    NOT NULL
);
'''
}

insertTables = {
'soldout':'''
INSERT INTO soldout(
article_id,
brand_name,
art_name,
stock_qty,
stock_location,
last_import,
supply_id,
year,
month,
date,
week,
weekday,
yyyymmdd,
humandate
)
VALUES (
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?
);
''',
'turnover_daily':'''
INSERT INTO turnover_daily
    (sum,year,month,date,week,weekday,yyyymmdd,humandate)
VALUES
    (?, ?, ?, ?, ?, ?, ?, ?);
''',
'brands':'''
INSERT INTO `brands`
    (`brand_id`, `brand_name`)
VALUES
    (?, ?);
''',
'articles':'''
INSERT INTO `articles`
    (article_id, brand_id, art_name)
VALUES
    (?, ?, ?);
'''
}



selectTables = {
'getItemsFromBrandId':'''
SELECT art_name
FROM articles
INNER JOIN brands
ON  brands.brand_id = articles.brand_id
WHERE brands.brand_id = '191';
'''

}
