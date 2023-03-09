# Overview for cocuvida
THIS DIRECTORY IS STILL UNDER DEVELOPEMENT

### Running
#### run normally
cd to OTGT/Energy_Management/cocuvida/app
```
python -m cocuvida
```
#### run with docker-compose
cd to OTGT/Energy_Management/cocuvida
```
docker-compose up cocuvida_prod
```

### Testing
#### run normally
cd to OTGT/Energy_Management/cocuvida/app
```
python -m tests
```
#### run with docker-compose
cd to OTGT/Energy_Management/cocuvida
```
docker-compose up cocuvida_test
```

### Developing Web Component
#### run normally
cd into OTGT/Energy_Management/cocuvida/app
```
uvicorn --port 8087 --reload cocuvida.web:app
```
#### run with docker-compose
cd to OTGT/Energy_Management/cocuvida
```
docker-compose up cocuvida_web
```
