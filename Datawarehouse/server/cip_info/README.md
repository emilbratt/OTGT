## About
This is the main webserver which also connects to the other services found within the OTGT/Datawarehouse/server/ directory


## Setting up the http server

### Install a headless Debian, make sure date/time are correct e.g.

Once you have an up and running system, follow these commands

Update system
```
sudo apt update && sudo apt upgrade -y
```

### Install dependencies and packages for SQL

For database dependencies for connecting to MSSQL and MariaDB database
```
sudo apt update && \
sudo apt install unixodbc -y && \
sudo apt install unixodbc-dev -y  && \
sudo apt install freetds-dev -y  && \
sudo apt install tdsodbc -y && \
sudo apt install freetds-bin -y && \
sudo apt install mariadb-server -y && \
sudo apt install apache2 php php-mysql libapache2-mod-php -y
```

start apache and mariadb
```
sudo systemctl enable mariadb apache2 && sudo systemctl start mariadb apache2
```

### Database connection and configurations
Add datasource for database connection
```
sudo nano /etc/freetds/freetds.conf
```

..and add text under inserting your correct parameters

```
[sqlserver]
  host = <ip/hostname> # database server
  port = 1433 # database port
  tds version = 7.4 # chose driver version
  instance = <databasename> # insert the name of the database
```
..save file and exit


Add config for FreeTDS
```
sudo nano /etc/odbcinst.ini  (add text under)
```
..and add text under inserting your correct parameters

```
[FreeTDS]
  Description = FreeTDS unixODBC Driver
  Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
  Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
  UsageCount = 1
```
..save file and exit

```
sudo nano  /etc/odbc.ini (add text under)
```
..add text under
```
[FreeTDS]
  Description = MSSQL Server
  Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
  Description = MSSQL Server
  Trace = No
  Server = <ip/hostname> # database server
  Database = <databasename> # database name
  Port = 1433 # database port
  TDS_Version = 7.4 # driver version
```
..save file and exit


### Apache Server Config

Open the virtual host config /etc/apache2/sites-available/datawarehouse.conf and point the document root to this directory using absolute path reference
```
DocumentRoot /var/www/html/OTGT/Datawarehouse/server/cip/document_root
```

Enable redirect for every request to index.php (change directory if needed)
```
<Directory "/var/www/html/OTGT/Datawarehouse/server/cip_info/document_root">
  # enable rewrite engine
  RewriteEngine On

  # set rewrite rule based on regex (1st flag) and call index.php (2nd flag with query string in $1 conserving the query string as stated in the 3rd flag)
  RewriteRule	^(.*)$	index.php?$1	[QSA,L]
</Directory>
```
..then save the virtual host config

Enable virtual host
```
sudo a2ensite datawarehouse
```

Enable mod_rewrite for apache to redirect all calls/urls/queries to webroot/index.php
```
sudo a2enmod rewrite
```


### Test connection from shell
issue this command from the same host as web-server (this host)
```
tsql -H <dbname> -p <port> -U sa -P <password>
```

### PHP ini

Open php ini for apache /etc/php/<php_version>/apache2/php.ini and uncomment / add lines
```
extension=pdo_odbc
extension=pdo_mysql
post_max_size = 20M
upload_max_filesize = 20M
```
