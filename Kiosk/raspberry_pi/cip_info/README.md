### Raspberry Pi kiosk mode for using the datawarehouse cip_info web-ui


* install raspberry pi os lite
* install git
```
sudo apt update && sudo apt install git -y
```
* run sudo raspi-config to:
```
setup ssh for connecting
set autologin
setup wifi if needed
 ```
* git clone this repo and navigate to this directory)
* run setup.sh as normal user (no sudo or root)
