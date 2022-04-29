### Raspberry Pi for registering shelf value for item


* install raspberry pi os lite
* install git
```
sudo apt update && sudo apt install git -y
```
* setup autologin to console
```
sudo raspi-config
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
