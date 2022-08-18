## spin up containers for developing

### setup
* make sure to have docker and docker-compose installed on your system
* make sure your user is part of the Docker group (no sudo here)
* create the environment.ini and place it in the root of the repository by copying and ediiting the environment.ini.template (also in the root of repository)
* configure Apache, ODBC and PHP from inside cip_info/
* start all services by running from this directory: $ docker-compose up
* restore datawarehouse database to [db_datawarehouse container](#db_datawarehouse)
* restore retail database to [db_retail container](#db_retail)
* and optionally see commands options regarding [docker-compose](#docker-compose) and/or overview of directories [directories](#directory-overview)

### docker-compose
start containers
```
docker-compose up
```
or as daemon (no log output)
```
docker-compose up -d
```
start containers and force rebuild
```
docker-compose up --no-deps --build
```
daemon
```
docker-compose up -d --no-deps --build
```
stop containers
```
docker-compose down
```
stop containers and remove docker volumes declared in docker-compose.yml
```
docker-compose down -v
```

### cip_info
* changes to PHP and Apache configs can be done inside the cip_info before starting containers

### db_datawarehouse
copy over sql script from host to the root directory inside container
```
docker cp ./script.sql db_datawarehouse:/script.sql
```
open a shell inside the container
```
docker exec -u 0 -it db_datawarehouse  bash
```
if database need to be specified (example uses CIP)
```
mysql -pmypassword CIP < /script.sql
```
if not
```
mysql -pmypassword < /script.sql
```
when done, exit container
```
exit
```

### db_retail
* restore database from MS SQL database by running script restore.sh inside directory db_retail/
* [MS SQL Docs](https://docs.microsoft.com/en-us/sql/linux/new-to-sql-learning-resources?view=sql-server-ver16)
* [MS SQL 2019 Container](https://docs.microsoft.com/en-gb/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash)
* [MS SQL Backup & Restore](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-migrate-restore-database?view=sql-server-linux-ver15)
* [MS SQL Restore backup to Docker](https://docs.microsoft.com/en-us/sql/linux/tutorial-restore-backup-in-sql-server-container?view=sql-server-linux-ver15)

### directory overview
<pre>
docker/ -> run "docker-compose up" from here to start
  |
  ├── barcode_generator/ -> Dockerfile and requirements for the Python FastAPI backend
  |
  ├── cip_info/ -> configs for the main web server that users interact with
  |                           
  ├── db_datawarehouse/ -> Dockerfile and init script for MariaDB datawarehouse database
  |                           
  └── db_retail/ -> Dockerfile and restore database script for the MS SQL retail database
</pre>
