# Overview for cocuvida
THIS DIRECTORY IS STILL UNDER DEVELOPEMENT

## developing and using cocuvida
### start application
run normally
cd to OTGT/Energy_Management/cocuvida/app
```
python -m cocuvida
```
run with docker-compose
cd to OTGT/Energy_Management/cocuvida
```
docker-compose up cocuvida_prod
```

### testing
run normally
cd to OTGT/Energy_Management/cocuvida/app
```
python -m tests
```
run with docker-compose
cd to OTGT/Energy_Management/cocuvida
```
docker-compose up cocuvida_test
```

### developing the web component (start web server)
run normally
cd into OTGT/Energy_Management/cocuvida/app
```
uvicorn --port 8087 --reload cocuvida.web:app
```
run with docker-compose
cd to OTGT/Energy_Management/cocuvida
```
docker-compose up cocuvida_web
```
