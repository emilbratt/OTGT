# The Mosquitto MQTT broker
* connecting smart controllers to smart devices (switches, lights, relays etc.)

NOTE: the "./bindmount" directory should be in the gitignore list and thus
created when running setup.sh

## Setup
1. cd into this directory

2. run setup.sh
```
./setup.sh
```

## ekstra options for administrating mosquitto
Start mosquitto
```
docker-compose up -d
```

add user and password
```
docker-compose exec mosquitto mosquitto_passwd -b /mosquitto/config/password.txt <user> <password>
```

delete user
```
docker-compose exec mosquitto mosquitto_passwd -D /mosquitto/config/password.txt <username>
```
