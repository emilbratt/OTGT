## About
requests from cip_info (or any device on local network) can send request
to the python fastapi backend for generating barcodes

barcodes will be generated and served based on specified api requests


### dependencies
* the barcode backend does not need to run as http user and therefore we use default user
install python dependencies with user that has uid 1000
```
pip3 install --user fastapi
pip3 install --user pydantic
pip3 install --user uvicorn
pip3 install --user aiofiles
pip3 install --user requests
pip3 install --user python-barcode
pip3 install --user Pillow
```

### create service for fastapi uvicorn
* discussed here https://github.com/encode/uvicorn/issues/678#issuecomment-1067208966
create a new service file
```
sudo nano /etc/systemd/system/barcode-generator.service
```
add below content and change needed values for user and path's
```
[Unit]
Description=barcode generator back-end
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
  barcode_generator.main:app \
  --reload \
  --host 0.0.0.0 \
  --port 8081

ExecReload=/bin/kill -HUP ${MAINPID}
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target
```
enable and start the fastapi back-end
```
sudo systemctl enable barcode-generator
sudo systemctl start barcode-generator
```
check status with
```
systemctl status barcode-generator
```
