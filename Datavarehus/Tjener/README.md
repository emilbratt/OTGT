<h3>Setup Autoreporting</h3>

Install a headless Debian and set password, set date/time etc then follow below

Update system
```
sudo apt update && sudo apt upgrade -y
```

Install mariadb
```
sudo apt install mariadb-server -y
```

Check if mariadb is up and running
```
sudo systemctl status mariadb
```


Install dependencies and packages for SQL
For python to write excel spreadshes
$ sudo apt install python3-openpyxl -y

For backup using rsync
$ sudo apt install rsync -y

For database dependencies for connecting to MSSQL database
```
sudo apt update && \
sudo apt install unixodbc -y && \
sudo apt install unixodbc-dev -y  && \
sudo apt install freetds-dev -y  && \
sudo apt install tdsodbc -y && \
sudo apt install freetds-bin -y  && \
sudo apt install python3-pip -y  && \
sudo apt install python-pyodbc
```

For python to connect to mariadb
```
sudo apt-get install libmariadb3 libmariadb-dev -y && \
pip3 install --user mariadb
```


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


Remove no more needed default settings for MariaDB
```
sudo mysql_secure_installation
```

Setting up the datawarehouse database
```
sudo mariadb
```


Here are some instructions for basic usage of mariadb

Create database (set your own name instead of DBNAME)
```
CREATE DATABASE IF NOT EXISTS DBNAME;
```
Add user that can do everything but only connect from the same machine
```
CREATE USER 'admin'@localhost IDENTIFIED BY 'password';
```
Add user that can read and access from everywhere..
```
CREATE USER 'readuser'@'%' IDENTIFIED BY 'password';
```
Add user that can read, update and insert from everywhere..
```
CREATE USER 'postuser'@'%' IDENTIFIED BY 'password';
```

Granting access to users
```
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
GRANT SELECT ON DBNAME.* TO 'readuser'@'%';
GRANT SELECT ON DBNAME.* TO 'postuser'@'%';
GRANT UPDATE ON DBNAME.* TO 'postuser'@'%';
GRANT INSERT ON DBNAME.* TO 'postuser'@'%';
```

reload for changes to take effect
```
FLUSH PRIVILEGES;
```

Delete user
```
DROP USER 'admin'@'localhost';
DROP USER 'readuser'@'%';
```

Allow remote connections
```
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
Remove (un-comment) bind restriction on localhost by commenting..
```
bind-address            = 127.0.0.1
```
To
```
# bind-address            = 127.0.0.1
```

Re(start) database
```
sudo systemctl restart mariadb
```

Add a MySQL/MariaDB configuration file -> (cnf-file)
```
nano ~/.my.cnf
```

add text
```
[mysqldump]
  user = db_user
  password = db_password
```
..and save file

fix permissions for database access
```
chmod 600 ~/.my.cnf
```

Create backup folder for database
```
mkdir ~/path/datawarehouse/db_backup
```

Make app folder and put app-source (files) in your users home folder
```
mkdir ~/path/datawarehouse
```

Copy files to this folder..


Rsync folder ../Data to cloud
```
ssh-keygen -t rsa -b 4096 -f $1 -q -N ""
```

Swap out username and host/ip and have ssh copy the public key to remote host
```
ssh-copy-id username@host/ip
```

Open crontab
```
crontab -e
```

add line (insert your remote hosts username)
```
0 3 * * * rsync -au  --bwlimit=2000 --log-file=~/rsync_Output.log -e "ssh -p 22" "~/Output"   user@host:/home/user/salesreport/
```

add salesreport folder on remote host
```
ssh user@user@host/ip -t mkdir salesreport
```

And exit
```
exit
```

Add crontab tasks
```
crontab -e
```

add text (swap out username, database_user, database_name e.g. with correct ones)
```
# run daily autoreport
20 1 * * * /usr/bin/python3 ~/path/datawarehouse/main.py

# send reports to remote_host
30 1 * * * rsync -au  --bwlimit=2000 --log-file=/home/username/rsync_Output.log -e "ssh -p 22" ~/path/datawarehouse/Data   username@remote_host.no:/home/username/salesreport/

# send log to remote_host
40 1 * * * rsync -au  --bwlimit=2000 --log-file=/home/username/rsync_Output.log -e "ssh -p 22" ~/path/datawarehouse/log   username@remote_host.no:/home/username/salesreport/

# do a mysql_dump
0 1 * * * mysqldump --single-transaction -h localhost -u database_user database_name >  /home/username/path/datawarehouse/db_backup/database_name_`date +"\%Y"`-`date +"\%m"`.bak

# send mysql_dump to remote_host
10 1 * * * rsync -au  --bwlimit=2000 --log-file=/home/username/rsync_mysqldumpp.log -e "ssh -p 22" /home/username/path/datawarehouse/db_backup   username@remote_host.no:/home/username/salesreport/

```

..and save file


Alternative to cron
Make boot script to run after boot -> for multi-user (systemd)
Swap out nameofservice with your preferred name
```
nano nameofservice.service
```

add this and tweak to your need
```
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
```

Enable and start service (remember to use your name)
```
sudo cp nameofscript.service /etc/systemd/system/nameofscript.service
sudo systemctl enable nameofscript.service
sudo systemctl start nameofscript.service
```
