# mosquitto and an mqtt client


### preparing and running mosquitto container
1. cd into this directory

2. run setup.sh (will eventually run docker-compose up -d)

## handy commands for configuring mosquitto
Start services
```
docker-compose up -d
```

start only mosquitto
```
docker-compose up -d mqtt_mosquitto
```

add user and password for mosquitto
```
docker-compose exec mosquitto mosquitto_passwd -b /mosquitto/config/password.txt <user> <password>
```

delete user for mosquitto
```
docker-compose exec mosquitto mosquitto_passwd -D /mosquitto/config/password.txt <username>
```
