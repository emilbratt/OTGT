# Overview for elprice

THIS DIRECTORY IS STILL UNDER DEVELOPEMENT

### directory overview
```
OTGT/Energy_Management/elprice
  |
  ├── fetch_elspot/ -> fetching elspot prices and send (raw & formatted data) to web_datastore
  |
  ├── generate_plot/ -> charts for visualizing elsopt prices
  |
  ├── generate_states/ -> generate states (power on/off or power-level) for miscellaneous devices based on elspot data
  |
  ├── mqtt_distribute/ -> publishes up-to-date data via MQTT (elspot, charts, power-states)
  |
  └── web_datastore/ -> middleware receiving, storing and serving data to and from all services
```

### configuration
1. this application depends on the mosquitto service (mqtt broker) in /OTGT/Energy_Management/mosquitto
2. before starting the containers, copy /OTGT/environment.ini.template -> /OTGT/environment.ini
3. then add config under section "mqtt" that points to a running instance of mosquitto
