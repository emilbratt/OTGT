# Overview for elprice

THIS DIRECTORY IS STILL UNDER DEVELOPEMENT

### directory overview
```
OTGT/Energy_Management/elprice
  |
  ├── fetch_elspot/ -> fetching elspot prices and send (raw & formatted data) to web_datastore
  |
  ├── generate_plot/ -> generate plot from elsopt prices
  |
  ├── generate_sensor/ -> generate states (power on/off or power-level) for any electric device
  |
  ├── mqtt_client/ -> fetch prices from restapi and publish to mqtt-broker
  |
  └── web_datastore/ -> middleware receiving, storing and serving data to and from all services
```
