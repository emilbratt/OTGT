### Raspberry Pi for registering shelf value for item

### Installation
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


### How to use
Connect LED to pin 17 and Ground.
and connect barcode scanner to USB.
Then connect power to device and wait for the LED to start blinking.

The device invokes application/interface.py in the foreground.
This is the "interface" for the user.

When you see the LED turn on and blink, you are ready.

Start by scanning item first then shelf.
The LED will blink faster when it expects a shelf.

You can also scan multiple items sequencally.
If you scan an item when the device expects a shelf, it turns on the "sequence mode"
The LED will turn ON (no blinking) reporting that you are scanning a sequence
When you are done, just scan a shelf.
All items from the sequence will be assigned to that shelf.
LED goes back to normal blinking expecting another item.

Everything else happens in the background by the application/daemon.py.
that is invoked as a background task by systemd.
You do not need to do anything in addition to scanning items and shelves.

Disconnect power when done (no need for gracefull power off here)
