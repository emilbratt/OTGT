# Overview for cocuvida
THIS DIRECTORY IS STILL UNDER DEVELOPEMENT

### Dependencies
All external Python dependencies are listed in requirements.txt

### Running cocuvida on host machine
cd to OTGT/Energy_Management/cocuvida/app
#### run all services
```
python -m cocuvida
```
#### run single service (example runs controlplan daemon)
```
python -m cocuvida controlplan
```

### Running cocuvida inside docker
cd to OTGT/Energy_Management/cocuvida
#### run all services (normal)
```
docker compose up cocuvida
```
#### run all services (test)
```
docker compose up cocuvida_all
```
#### run a specific service (example starts the web "cocuvida_web" container)
```
docker compose up cocuvida_web
```

### Testing on host machine
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

### Testing inside docker
cd to OTGT/Energy_Management/cocuvida
#### run all tests
```
docker compose up cocuvida_test
```

### Developing Web Component
#### Starting ASGI server on host machine
cd into OTGT/Energy_Management/cocuvida/app
```
uvicorn --port 8087 --reload cocuvida.web:app
```
#### Starting ASGI server with docker compose (will use uvloop instead of asyncio for event loops)
cd to OTGT/Energy_Management/cocuvida
```
docker compose up cocuvida_web
```
