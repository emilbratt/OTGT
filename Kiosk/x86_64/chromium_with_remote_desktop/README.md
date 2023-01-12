### Install Debian
1. grab iso from https://www.debian.org/distrib/

2. use dd and write iso to USB
```
sudo dd if=$ISO_FILE of=$USB_DEVICE_PATH bs=8192k
```

3. insert, install and proceed

### Install base software on fresh Debian install
switch to root
```
su
```
install basic components
```
apt update && apt upgrade -y && apt-get install sudo gnupg git rfkill -y
```

give your user sudo privileges (swap out <user> and match yours)
```
/sbin/usermod -aG sudo <user>
```

reboot
```
/sbin/reboot
```

### install xorg, openbox and chromium
```
sudo apt-get install xserver-xorg x11-xserver-utils xinit xbase-clients openbox chromium -y
```

### install chromium autostart for openbox
```
sudo nano /etc/xdg/openbox/autostart
```

insert and match settings for your needs
```
xset s off
xset s noblank
xset -dpms
setxkbmap -option terminate:ctrl_alt_bksp
chromium --disable-features=TranslateUI --noerrdialogs --disable-infobars --start-fullscreen 'https://google.com'
```

reboot
```
sudo reboot
```

### install teamviewer remote desktop
* note: we have to use the command-line setup because teamviewer sub-menu windows
does not play nicely with openbox making configuration hard/impossible using the gui
* once setup, remote connections however; will work just fine

```
wget https://download.teamviewer.com/download/linux/teamviewer-host_amd64.deb
sudo apt install ./teamviewer-host_amd64.deb
```
if missing dependencies
```
sudo apt --fix-broken install
```

THIS COMMAND HAS TO BE RUN LOCALLY (it will fail with a connection error if run through an ssh connection)
```
sudo teamviewer setup
```

reboot
```
sudo reboot
```

* if any problem during "sudo teamviewer setup"

if connection error during setup and using ipv4
```
sudo nano /etc/sysctl.conf
```

insert
```
net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.lo.disable_ipv6=1
```

for fixing PPA teamviewer, file located
```
sudo nano /etc/apt/sources.list.d/teamviewer.list
```

reboot and try "sudo teamviewer setup" again
```
sudo reboot
```

### install lightdm window manager (greeter) for autologin etc.
```
sudo apt-get install lightdm lightdm-gtk-greeter-settings -y
```

add new user (swap out <user> with the one you want)
```
sudo adduser <user>
```

configure autologin
```
sudo nano /etc/lightdm/lightdm.conf
```

insert and match settings for your needs
```
[Seat:*]
user-session=openbox

autologin-user=<user>
autologin-user-timeout=10

greeter-show-manual-login=true
allow-guest=false
greeter-hide-users=true
```

reboot
```
sudo reboot
```

### isntall vnc remote desktop
```
sudo apt install x11vnc -y
```

create password for vnc using the lightdm user (which owns the x-session)
```
sudo -u lightdm x11vnc -storepasswd
```

create systemd service for vnc (make sure to match your needs)
```
sudo nano /etc/systemd/system/x11vnc_autostart.service
```

insert and match settings for your needs
```
[Unit]
Description=VNC Remote desktop
After=display-manager.service

[Service]
Type=simple
User=lightdm
ExecStart=/usr/bin/x11vnc -rfbauth /var/lib/lightdm/.vnc/passwd -display %i
Restart=always
RestartSec=3

[Install]
WantedBy=graphical.target
```

enable vnc sytemd service
```
sudo systemctl enable x11vnc_autostart
```

reboot
```
sudo reboot
```
