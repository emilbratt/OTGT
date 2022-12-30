# Overview for Energy Management

THIS DIRECTORY IS STILL UNDER DEVELOPEMENT AND SERVES AS A GUIDELINE FOR NOW

* this directory contains software used to control smart devices
* each directory contains its own service in the form of a docker-compose.yml file
* the services do not have to be run on the same node/host
* for production, please copy the directories out of the repo and make adjustments to match your environment

### read the README.md file in its corresponding directory before doing anything inside it

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
