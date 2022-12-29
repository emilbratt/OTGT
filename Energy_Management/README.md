# Overview for Energy Management

THIS DIRECTORY IS STILL UNDER DEVELOPEMENT

* this directory contains software used to control smart devices
* each directory contains its own service in the form of a docker-compose.yml file
* the services do not have to be run on the same node/host


### directory overview Energy Management
<pre>
Energy_Management/ -> directory where this file resides
  |
  ├── elprice/ -> fetching and processing elspot prices
  |
  ├── homeassistant/ -> the Home Assistant core
  |
  └── mosquitto/ -> the mosquitto MQTT broker for IoT message delivering
</pre>
