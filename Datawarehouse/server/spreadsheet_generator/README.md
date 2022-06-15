## About
powered by:
[Uvicorn ASGI server](https://www.uvicorn.org/)
[Python FastAPI backend](https://fastapi.tiangolo.com/)
[Pydantic datamodel](https://pydantic-docs.helpmanual.io/)
[Python openpyxl](https://pypi.org/project/openpyxl/)

any device on local network can send request to the python fastapi backend
for generating spreadsheets from json arrays

### dependencies
* the backend can and must run as default user with uid 1000
install python dependencies with user that has uid 1000
```
pip3 install --user fastapi
pip3 install --user pydantic
pip3 install --user uvicorn
pip3 install --user aiofiles
pip3 install --user requests
pip3 install --user openpyxl
```

### create service for fastapi uvicorn
* discussed here https://github.com/encode/uvicorn/issues/678#issuecomment-1067208966
create a new service file
```
sudo nano /etc/systemd/system/spreadsheet-generator.service
```
add below content and change needed values for user and path
```
[Unit]
Description=spreadsheet generator back-end
After=network.target

[Service]
Type=simple
User=bob
Group=bob

# uncomment below to force read only file system; read more here https://0pointer.net/blog/dynamic-users-with-systemd.html
# DynamicUser=true #
# PrivateTmp=true #

WorkingDirectory=/path/to/OTGT/Datawarehouse/server
EnvironmentFile=/path/to/OTGT/environment.ini

ExecStart=/home/bob/.local/bin/uvicorn \
  spreadsheet_generator.main:app \
  --reload \
  --host 0.0.0.0 \
  --port 8082

ExecReload=/bin/kill -HUP ${MAINPID}
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target
```
enable and start the fastapi back-end
```
sudo systemctl enable spreadsheet-generator
sudo systemctl start spreadsheet-generator
```
check status with
```
systemctl status spreadsheet-generator
```

starting manually can be done navigating to OTGT/Datawarehouse/server and running
```
uvicorn spreadsheet_generator.main:app --reload --host 0.0.0.0 --port 8081
```
make sure uvicorn is in PATH

follow journal (log output) for debugging
```
sudo journalctl -fu spreadsheet-generator.service
```
