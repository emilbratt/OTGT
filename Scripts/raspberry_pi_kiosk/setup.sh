#!/usr/bin/env bash
#────────────────────────────────────────────#
# Author:
#   Emil Bratt Børsting
#────────────────────────────────────────────#
# Description:
#   automatically setup kiosk running chromium
#────────────────────────────────────────────#
# Customization of this script
#   add dependencies (files) and make sure they
#   are listed in the DEPENDENCIES variable
#────────────────────────────────────────────#

declare DEPENDENCIES

DEPENDENCIES=(
  autostart
  keyboard
  wifisignal
)

function check_dependencies () {
  for file in "${DEPENDENCIES[@]}"
  do
    if [[ ! -f ./$file ]]; then
      echo "cannot find $file (should be in the same directory as this script"
      exit 1
    fi
  done
}

# ensure dependencies are met before continuing
if [[ ! -f ./autostart ]]; then
  echo 'cannot find autostart script (should be in the same directory as this script'
  exit 1
fi
if [[ ! -f ./keyboard ]]; then
  echo 'cannot find keyboard config (should be in the same directory as this script'
  exit 1
fi


function internet_reachable () {
  wget -q --spider http://google.com
  if [ $? -eq 0 ]; then
    return 0
  fi
  echo 'Make sure to have internet access before running this script'
  exit 1
}

function set_password () {
  echo 'Set new password'
  passwd
}

function setup_hostname () {
  NEW_HOSTNAME=$(cat /etc/hostname)
  read -e -i "$NEW_HOSTNAME" -p "Hostname (use backspace to erase and set new): " input
  NEW_HOSTNAME="${input:-$NEW_HOSTNAME}"
  echo $NEW_HOSTNAME | sudo tee /etc/hostname
}

function system_update () {
  sudo apt-get update && sudo apt-get upgrade -y
}

function setup_software () {
  # install chromium and x-server
  sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox -y
  sudo apt-get install --no-install-recommends chromium-browser -y
  sudo apt-get install xbase-clients -y
}

function setup_start_command () {
  # set startup command for profile
  cat /home/pi/.bash_profile | grep -q 'startx'
  if [[ $? -eq 1 ]]; then
    echo 'if [ -z $DISPLAY ] && [ "$(tty)" = "/dev/tty1" ]; then startx; fi' >> /home/pi/.bash_profile
  fi
}

function set_locale () {
  cat /etc/locale.gen | grep -wq 'nb_NO.UTF-8 UTF-8'
  if [[ $? -eq 1 ]]; then
    echo 'nb_NO.UTF-8 UTF-8' | sudo tee -a /etc/locale.gen
  fi
  sudo locale-gen nb_NO.UTF-8 UTF-8
  sudo update-locale nb_NO.UTF-8 UTF-8
  # export LANGUAGE=en_GB.UTF-8
  # export LC_ALL=nb_NO.UTF-8
  # sudo dpkg-reconfigure locales
}

function transfer_dependencies () {
  # copy over the autostart config for cor starting chromium correctly on x
  sudo cp -f ./autostart /etc/xdg/openbox/
  # copy over the keyboard config for noewegian keyboard
  sudo cp -f ./keyboard /etc/default/keyboard
  # copy over the convenience script for checking signal strength
  sudo cp -f ./wifisignal /usr/local/bin/
}


check_dependencies
internet_reachable
set_password
setup_hostname
system_update
setup_software
setup_start_command
set_locale
transfer_dependencies
sudo reboot
