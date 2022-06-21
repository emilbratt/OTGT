## spin up containers for developing

### setup
* make sure to have docker and docker-compose installed on your system
* create the environment.ini file using the template -> environment.ini.template

### commands
* start containers
```
docker-compose up
# or as daemon (no log output)
docker-compose up -d
```
* start containers and force rebuild
```
docker-compose up --no-deps --build
# daemon
docker-compose up -d --no-deps --build
```
* stop containers
```
docker-compose down
```
* stop containers and remove docker volumes declared in docker-compose.yml
```
docker-compose down -v
```

### cip_info
* change configs can be done inside the cip_info directory

### db_datawarehouse
* adding and running sql script on service db_datawarehouse (commands below need tweaking)
```
# copy over sql script from host to the root directory inside container
docker cp ./script.sql db_datawarehouse:/script.sql
# open a shell inside the container
docker exec -u 0 -it db_datawarehouse  bash
# if database need to be specified (example uses CIP)
mysql -pmypassword CIP < /script.sql
# if not
mysql -pmypassword < /script.sql
# when done, exit container
exit
```

### directory overview
<pre>
docker/ -> run "docker-compose up" from here to start
  |
  ├── barcode_generator/ -> Dockerfile and requirements for the Python FastAPI backend
  |
  ├── cip_info/ -> configs for the main web server that users interact with
  |                           
  └── db_datawarehouse/ -> Dockerfile and init script for datawarehouse database
</pre>
