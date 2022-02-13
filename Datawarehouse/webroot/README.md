## About
This is the webserver that brings some functionality to the user such as reading values from the POS database and reports


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
  host = <ip/hostname> # Remote Sql Server's IP addr
  port = 1433 # this is default port, but you can change it
  tds version = 7.4 # chose version you want to use
  instance = <dbname> # insert the name of the database you are gonna use
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
  Server = <ip/hostname> # IP or host name of the Sql Server
  Database = <DBNAME> # Database name
  Port = 1433 # this is default port, but you can change it
  TDS_Version = 7.4 # chose version you want to use
```
..save file and exit
