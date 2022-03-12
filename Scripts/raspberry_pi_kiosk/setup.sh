#!/usr/bin/env bash

# ensure dependencies are met before continuing
if [[ ! -f ./autostart ]]; then
  echo 'cannot find autostart script (should be in the same directory as this script'
  exit 1
fi
if [[ ! -f ./keyboard ]]; then
  echo 'cannot find keyboard config (should be in the same directory as this script'
  exit 1
fi

# set hostname
NEW_HOSTNAME=$(cat /etc/hostname)
read -e -i "$NEW_HOSTNAME" -p "Hostname (use backspace to erase and set new): " input
NEW_HOSTNAME="${input:-$NEW_HOSTNAME}"
echo $NEW_HOSTNAME | sudo tee /etc/hostname

# update system
sudo apt update && sudo apt upgrade -y

# install chromium and x-server
sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox -y
sudo apt-get install --no-install-recommends chromium-browser -y
sudo apt-get install xbase-clients -y

# set startup command for profile
cat /home/pi/.bash_profile | grep -q 'startx'
if [[ $? -eq 1 ]]; then
  echo 'if [ -z $DISPLAY ] && [ "$(tty)" = "/dev/tty1" ]; then startx; fi' >> /home/pi/.bash_profile
fi

# copy over the autostart config for cor starting chromium correctly on x
sudo cp -f ./autostart /etc/xdg/openbox/
# copy over the keyboard config for noewegian keyboard
sudo cp -f ./keyboard /etc/default/keyboard



# reboot
sudo reboot