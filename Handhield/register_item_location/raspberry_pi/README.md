### Raspberry Pi for registering shelf value for item


* install raspberry pi os lite
* install git
```
sudo apt update && sudo apt install git -y
```
* if neeeded, run sudo raspi-config to:
```
setup ssh for connecting
set autologin
setup wifi if needed
 ```

* setup application
```
cd && git clone https://github.com/emilbratt/OTGT.git
```
```
cd OTGT/Handhield/register_item_location/raspberry_pi
```
```
./setup.sh
```
