<h3>Setup</h3>

Install a headless Debian
Enable ssh, generate ssh-keys, set password and set date/time etc..

Update system
$ sudo apt update && sudo apt upgrade -y

Install mariadb
$ sudo apt install mariadb-server -y

Check if mariadb is up and running
$ sudo systemctl status mariadb
If up and running, press q to quit

Remove unecessary default options and settings for security
$ sudo mysql_secure_installation


Install dependencies and packages for SQL
For python to write excel spreadshes
$ sudo apt install python3-openpyxl -y

For backup using rsync
$ sudo apt install rsync -y

For python to connect to MSSQL
$ sudo apt install unixodbc -y
$ sudo apt install unixodbc-dev -y
$ sudo apt install freetds-dev -y
$ sudo apt install tdsodbc -y
$ sudo apt install freetds-bin -y
$ sudo apt install python3-pip -y
$ sudo apt install python-pyodbc

For python to connect to mariadb
$ sudo apt-get install libmariadb3 libmariadb-dev -y
$ pip3 install --user mariadb


Add freetds driver to datasource
$ sudo nano /etc/freetds/freetds.conf

(add text under)

[sqlserver]
      host = <ip/hostname> # Remote Sql Server's IP addr
      port = 1433 # this is default port, but you can change it
      tds version = 7.4 # chose version you want to use
      instance = <dbname> # insert the name of the database you are gonna use

(save and exit)


$ sudo nano /etc/odbcinst.ini  (add text under)

(add text under)

[FreeTDS]
Description = FreeTDS unixODBC Driver
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
UsageCount = 1

(save and exit)


$ sudo nano  /etc/odbc.ini (add text under)

(add text under)

[FreeTDS]
Description = MSSQL Server
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Description = MSSQL Server
Trace = No
Server = <ip/hostname> # IP or host name of the Sql Server
Database = <DBNAME> # Database name
Port = 1433 # this is default port, but you can change it
TDS_Version = 7.4 # chose version you want to use

(save and exit)


Prepare for production environment
$ sudo mysql_secure_installation

Setting up the datawarehouse database
$ sudo mariadb


#### Instructions for basic usage of mariadb ####

Create database (set your own name instead of DBNAME)
```
  CREATE DATABASE IF NOT EXISTS DBNAME;
```
Add user
-> can do everything but only connect from the same machine
# CREATE USER 'admin'@localhost IDENTIFIED BY 'password';

-> can read and access from everywhere..
# CREATE USER 'readuser'@'%' IDENTIFIED BY 'password';

-> can read, update and insert from everywhere..
# CREATE USER 'postuser'@'%' IDENTIFIED BY 'password';


Granting access

# GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';

# GRANT SELECT ON DBNAME.* TO 'readuser'@'%';

# GRANT SELECT ON DBNAME.* TO 'postuser'@'%';
# GRANT UPDATE ON DBNAME.* TO 'postuser'@'%';
# GRANT INSERT ON DBNAME.* TO 'postuser'@'%';

reload for changes to take effect
# FLUSH PRIVILEGES;

Delete user
# DROP USER 'admin'@'localhost';
# DROP USER 'readuser'@'%';


Allow remote connections
$ sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
Remove bind restriction on localhost by commenting..
bind-address            = 127.0.0.1
To
# bind-address            = 127.0.0.1

$ sudo systemctl restart mariadb

Add a MySQL/MariaDB configuration file -> (cnf-file)
$ nano ~/.my.cnf

(add text)

[mysqldump]
user = db_user
password = db_password

(save)

$ chmod 600 ~/.my.cnf

Create backup folder for database
$ mkdir ~/autoreport/db_backup

Make app folder and put app-source (files) in your users home folder
$ mkdir ~/autoreport
Copy files to this folder..





Rsync folder ../Data to cloud
$ ssh-keygen -b 4096
    --press enter all way thorugh
$ ssh-copy-id username@host/ip
crontab -e
0 3 * * * rsync -au  --bwlimit=2000 --log-file=~/rsync_Output.log -e "ssh -p 22" "~/Output"   user@host:/home/user/dir/
ssh user@user@host/ip
mkdir salesreport
exit


Add crontab tasks
$ crontab -e

(add text)

# do a daily mysql_dump with a weekly name_stamp
0 1 * * * mysqldump --single-transaction -h localhost -u databaseuser CIP >  /home/username/autoreport/db_backup/DB_NAME_`date +"\%Y"`-`date +"\%m"`_week-`date +"\%V"`.bak

# send mysql_dump to cloud
10 1 * * * rsync -au  --bwlimit=2000 --log-file=/home/username/rsync_mysqldumpp.log -e "ssh -p 22" /home/username/autoreport/db_backup   username@hostname:/home/username/salesreport/

# run daily autoreport
20 1 * * * /usr/bin/python3 ~/autoreport/main.py

# send reports to cloud
40 1 * * * rsync -au  --bwlimit=2000 --log-file=/home/username/rsync_Output.log -e "ssh -p 22" ~/autoreport/Data   username@hostname:/home/username/salesreport/

# send aytoreport log to cloud
50 1 * * * rsync -au  --bwlimit=2000 --log-file=/home/username/rsync_Output.log -e "ssh -p 22" ~/autoreport/log   username@hostname:/home/username/salesreport/

(save)


optional...

Make boot script to run after boot -> for multi-user (systemd)
nano nameofscript.py
	write the script....


nano nameofscript.service
[Unit]
Description=what script does
After=multi-user.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/
Type=simple
ExecStart=/usr/bin/python3 /home/user/nameofscript.py
KillMode=process

[Install]
WantedBy=multi-user.target


sudo cp nameofscript.service /etc/systemd/system/nameofscript.service
sudo systemctl enable update_shelf.service
