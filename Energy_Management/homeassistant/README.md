# Installation Raspberry Pi (only tested on 3 b+)

Prepare a Raspberry Pi with Raspberry Pi OS Lite

do full system upgrade
```
sudo apt update && sudo apt full-upgrade -y
```

install docker see -> https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script
```
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
```

give user perm. to handle docker daemon - change pi to correct user if nescessary
```
sudo usermod -aG docker pi
```

install docker-compose
```
sudo apt install docker-compose -y
```

enable docker
```
sudo systemctl enable docker
```
reboot system
```
sudo reboot
```
