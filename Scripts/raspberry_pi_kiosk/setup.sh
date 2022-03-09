#!/usr/bin/env bash

# install raspberry pi os lite
# run sudo raspi-config to:
#   set locale settings
#   setup ssh for connecting
#   set autologin
#   setup wifi if needed

# run this script (you will be promted for password occasionally)

# update system
sudo apt update && sudo apt upgrade -y

# install chromium and x-server
sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox -y
sudo apt-get install --no-install-recommends chromium-browser -y
sudo apt-get install xbase-clients -y

# set startup command for profile
echo 'startx' >> /home/pi/.bash_profile

# copy over the autostart config for cor starting chromium correctly on x
if [[ ! -f ./autostart ]]; then
  echo 'cannot find autostart script (should be in the same directory as this script'
  exit 1
fi
sudo cp -f ./autostart /etc/xdg/openbox/
