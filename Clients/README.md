## This directory contains the "otgt" command/tools for employee's work computers

### I can add functionality via shell scripts that they in turn can run

### Prerequisites
* client computer needs to run Linux or MacOS
* client computer needs to have git installed
* clone this repository
* add this specific directory (abs path) to $PATH on boot

example line to use in e.g. .bashrc
```
PATH=$PATH:/path/to/OTGT/Clients
```

* after reboot or shell-refresh, we are able to run the app with this command
```
otgt
```
