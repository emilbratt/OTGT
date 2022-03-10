### Raspberry Pi kiosk mode for datawarehouse server


* install raspberry pi os lite
* run sudo raspi-config to:
 ```
 set locale settings
 setup ssh for connecting
 set autologin
 setup wifi if needed
 ```
* copy over the autostart and setuo.sh file to the same directory (or an esaier way: git clone this repo and navigate to this directory)
* run setup.sh as pi user
