
def prepareDB():
    pass


class Postrecords:
    def __init__(self):
        from credentials import loadCredentials
        credentials = loadCredentials('post')



    def articles(self):
        pass

    def barcodes(self):
        pass

    def soldout(self):
        pass

    def import(self):
        pass

    def storage(self):
        pass

    def turnover(self):
        '''
            update turnover_hourly and turnover_daily
            find a way to split the total from the hourly...
        '''
        pass


if __name__ == '__main__':
    pass


'''
SQL STATEMENTS...


Create and use database named yourdbname
################################
CREATE DATABASE IF NOT EXISTS yourdbname;
USE yourdbname;
################################




Create table for import
################################
CREATE TABLE IF NOT EXISTS import(
article_id  INT NOT NULL,
brand       VARCHAR(255)  NOT NULL,
name        VARCHAR(255)  NOT NULL,
stock_qty   INT           NULL,
location    VARCHAR(255)  NULL,
last_import VARCHAR(255),
FOREIGN KEY (article_id) REFERENCES articles(article_id)
);

################################
DESC import;
################################









# CREATE USER 'cipadmin'@'localhost' IDENTIFIED BY 'secret_password';
# CREATE USER 'cipread'@'%' IDENTIFIED BY 'secret_password';

# GRANT ALL PRIVILEGES ON cipadmin.* TO 'yourdbname'@'localhost';
# GRANT SELECT ON cipread.* TO 'yourdbname'@'%';

# FLUSH PRIVILEGES;




______________________


'''
