### This is the workdirectory for all things cocuvida
* Executing is done by running the select sub directory sa a python module from this directory

### Directory Overview
```
/OTGT/Energy_Management/cocuvida/
  |
  ├── cocuvida/ -> source code for cocuvida application
  |
  ├── tests/ -> unit tests that will load modules and run test cases for cocuvida (please run this before git pushing)
  |
  └── tools/ -> when you do not want to change the source code or the test code, debugging and testing can be done here
```

##### Run cocuvida and <optionally> specify service name for running only one service
```
python -m cocuvida <service>
```
##### Run tests and <optionally> include class name from "tests/__main__.py" for running only one test case
```
python -m tests <class>
```
##### Run tools
```
python -m tools
```
