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
enable ssh
enable console autologin
setup wifi
..
..

* git clone this repo and navigate to this directory)
```
git clone https://github.com/emilbratt/OTGT.git
```

* run setup.sh as normal user (no sudo or root)
```
cd OTGT/Kiosk/raspberry_pi/chromium/
./setup.sh
```
