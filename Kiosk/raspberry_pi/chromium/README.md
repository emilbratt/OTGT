### Raspberry Pi kiosk mode for chromium

* install raspberry pi os lite

* then install git with below command
```
sudo apt update && sudo apt install git -y
```

* use below command to run sudo raspi-config and make optional adjustments
```
sudo raspi-config
```
optional adjustments include:
setup ssh
set console autologin
setup wifi
set performance options
advanced options -> opengl

* git clone this repo and navigate to this directory)

* run setup.sh as normal user (no sudo or root)
