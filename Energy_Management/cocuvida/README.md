# Cocuvida  - (Co)ntrolling (Cu)rrents and (Vi)sualizing (Da)ta
#### this app is under developement
As of now, it is not in a working state
#### Dependencies
All external Python dependencies are listed in requirements.txt

## Run Cocuvida
### On host machine
cd to OTGT/Energy_Management/cocuvida/app
#### run all services
```
python -m cocuvida
```
#### run single service (example runs controlplan daemon)
```
python -m cocuvida controlplan
```
### Inside docker
cd to OTGT/Energy_Management/cocuvida
#### run all services (normal)
```
docker compose up cocuvida
```
#### run all services for developing or testing
```
docker compose up cocuvida_all
```
#### run a specific service (example starts the web "cocuvida_web" container)
```
docker compose up cocuvida_web
```

## Developing
### Unit-Testing on host machine
cd to OTGT/Energy_Management/cocuvida/app
#### run all tests
```
python -m tests
```
#### test one class module only - for example application configuration with the class Envrinoment
```
python -m tests Environment
```
#### test one method only - for example Envrinoment.test_environment_cocuvida
```
python -m tests Environment.test_environment_cocuvida
```
### Unit-Testing inside docker
cd to OTGT/Energy_Management/cocuvida
#### will run all tests
```
docker compose up cocuvida_test
```
### Developing Web Component (includes setting sane arguments like auto-reloading..)
#### Starting ASGI server on host machine
cd into OTGT/Energy_Management/cocuvida/app
```
uvicorn --lifespan on --log-level debug --use-colors --port 8087 --host 0.0.0.0 --reload cocuvida.web:app
```
#### Starting ASGI server with docker compose (will use uvloop instead of asyncio for event loops)
cd to OTGT/Energy_Management/cocuvida
```
docker compose up cocuvida_web
```

### Using Tools
#### Tooling on host machine
cd to OTGT/Energy_Management/cocuvida/app
```
python -m tools
```
#### Tooling inside docker
cd into OTGT/Energy_Management/cocuvida
```
docker compose up cocuvida_tools
```
