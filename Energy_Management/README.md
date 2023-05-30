# Overview for Energy Management

THIS DIRECTORY IS STILL UNDER DEVELOPEMENT AND SERVES AS A GUIDELINE FOR NOW

### IMPORTANT: before starting select containers
#### mosquitto
Make sure to have config ready in /OTGT/Energy_Management/mosquitto/bindmount/config
You can create these by cd'ing into /OTGT/Energy_Management/mosquitto and run setup.sh
#### zigbee2mqtt
Make sure to have config ready in /OTGT/Energy_Management/zigbee2mqtt/bindmount
You can create template by cd'ing into /OTGT/Energy_Management/zigbee2mqtt and runnig docker compose up
After starting and stopping, change the configuration.yaml file to fit your need
#### homeassistant
Make sure to have config ready in /OTGT/Energy_Management/homeassistant/bindmount
You can create template by cd'ing into /OTGT/Energy_Management/homeassistant and runnig docker compose up
After starting and stopping, edit the yaml files to match your needs

### run containers
cd to OTGT/Energy_Management
#### build/start/stop dev. containers
```
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up
docker compose -f docker-compose.dev.yml down
```
#### build/start/stop prod. containers
```
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up
docker compose -f docker-compose.prod.yml down
```
#### running select containers
You might not want to run all services (containers) listed in the docker compose files.
For instance, if you only want to run mosquitto and zigbee2mqtt,
then you can do so by specifying the service names in the command.
Example below..
```
docker compose -f docker-compose.prod.yml up mosquitto_prod zigbee2mqtt_prod
```

### directory overview
```
OTGT/Energy_Management/
  |
  ├── cocuvida/ -> controlling currents and visualizing data (our IoT application)
  |
  ├── homeassistant/ -> the Home Assistant core
  |
  ├── mosquitto/ -> IoT messaging (mosqutito mqtt-broker)
  |
  └── zigbee2mqtt/ -> control zigbee devices via mqtt
```
