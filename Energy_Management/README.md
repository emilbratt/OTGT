# Overview for Energy Management

THIS DIRECTORY IS STILL UNDER DEVELOPEMENT AND SERVES AS A GUIDELINE FOR NOW

### run docker containers
cd to OTGT/Energy_Management
#### build/start/stop dev. containers
```
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml down
```
#### build/start/stop prod. containers
```
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml down
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
