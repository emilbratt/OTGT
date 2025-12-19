#!/usr/bin/env bash
#────────────────────────────────────────────#
# Author:
#   Emil Bratt Børsting
#────────────────────────────────────────────#
# Description:
#   installs a kiosk running chromium
#────────────────────────────────────────────#

function check_internet_connection () {
  wget -q --spider http://google.com
  if [ $? -eq 0 ]; then
    return 0
  fi
  echo 'Make sure to have internet access before running this script'
  exit 1
}

function setup_hostname () {
  NEW_HOSTNAME=$(cat /etc/hostname)
  read -e -i "$NEW_HOSTNAME" -p "Hostname (use backspace to erase and set new): " input
  NEW_HOSTNAME="${input:-$NEW_HOSTNAME}"
  echo $NEW_HOSTNAME | sudo tee /etc/hostname
}

function system_update () {
  sudo apt-get update && sudo apt-get full-upgrade -y
}

function setup_software () {
  # install chromium and x-server
  sudo apt-get update && sudo apt-get install xorg chromium -y
}

function setup_start_command () {
  # set startup command for profile
  cat $HOME/.bash_profile | grep -q 'startx'
  if [[ $? -eq 1 ]]; then
    echo 'if [ -z $DISPLAY ] && [ "$(tty)" = "/dev/tty1" ]; then startx; fi' >> $HOME/.bash_profile
  fi
}

function set_locale () {
  cat /etc/locale.gen | grep -wq 'nb_NO.UTF-8 UTF-8'
  if [[ $? -eq 1 ]]; then
    echo 'nb_NO.UTF-8 UTF-8' | sudo tee --append /etc/locale.gen
  fi
  sudo locale-gen nb_NO.UTF-8 UTF-8
  sudo update-locale nb_NO.UTF-8 UTF-8
}

function transfer_dependencies () {
  # copy over the keyboard config for noewegian keyboard
  sudo cp -f keyboard /etc/default/keyboard
  # copy over the convenience script for checking signal strength
  sudo cp -f wifisignal /usr/local/bin/
}

function setup_init_script () {
  # copy over the xinit config for startx command for starting chromium correctly on xorg
  cp -f .xinitrc $HOME/.xinitrc

  # insert display resolution
  printf 'write the horizontal pixel width (example: 1920) and Enter: '; read DISPLAY_PIXEL_HORIZONTAL
  printf 'write the vertical pixel heihgt (example: 1080) and Enter: '; read DISPLAY_PIXEL_VERTICAL
  line_append="--window-size=${DISPLAY_PIXEL_HORIZONTAL},${DISPLAY_PIXEL_VERTICAL} \\"
  echo $line_append >> $HOME/.xinitrc

  # insert url to open on launch
  printf 'write the full URL for chromium to open on boot and press Enter: '; read URL_CHROMIUM
  line_append="'${URL_CHROMIUM}'"
  echo $line_append >> $HOME/.xinitrc
}


check_internet_connection
setup_hostname
system_update
setup_software
setup_start_command
set_locale
transfer_dependencies
setup_init_script
sudo reboot
