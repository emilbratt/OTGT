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
    read -p "Disable cursor? [y/N]: "  DISABLE_CURSOR
    if [[ $DISABLE_CURSOR =~ ^[Yy]$ ]]; then
        echo 'if [ -z $DISPLAY ] && [ "$(tty)" = "/dev/tty1" ]; then sleep 5; startx -- -nocursor; fi' >> $HOME/.bash_profile
    else
        echo 'if [ -z $DISPLAY ] && [ "$(tty)" = "/dev/tty1" ]; then sleep 5; startx; fi' >> $HOME/.bash_profile
    fi
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

  read -p "Do you want to rotate the screen 90 degrees (vertical view)? [y/N]: "  ROTATE_SCREEN
  if [[ $ROTATE_SCREEN =~ ^[Yy]$ ]]; then
  # copy over the rotation script
    sudo cp -f 10-monitor.conf /etc/X11/xorg.conf.d/10-monitor.conf
  fi
}

function setup_init_script () {
  # copy over the xinit config for startx command for starting chromium correctly on xorg
  cp -f .xinitrc $HOME/.xinitrc

  # insert display resolution
  printf 'Write the horizontal pixel width (example: 1920) and Enter: '; read DISPLAY_PIXEL_HORIZONTAL
  printf 'Write the vertical pixel heihgt (example: 1080) and Enter: '; read DISPLAY_PIXEL_VERTICAL

  read -p "Did you rotate the screen and now mixed up the width and height in the previous step? If so, do you want to swap horizontal and vertical values? [y/N]: "  SWAP_IT
  if [[ $SWAP_IT =~ ^[Yy]$ ]]; then
    line_append="--window-size=${DISPLAY_PIXEL_VERTICAL},${DISPLAY_PIXEL_HORIZONTAL} \\"
    echo $line_append >> $HOME/.xinitrc
  else
    line_append="--window-size=${DISPLAY_PIXEL_HORIZONTAL},${DISPLAY_PIXEL_VERTICAL} \\"
    echo $line_append >> $HOME/.xinitrc
  fi

  read -p "Do you want the web-content scaled? (bigger or smaller content) [y/N]: "  SCALE_IT
  if [[ $SCALE_IT =~ ^[Yy]$ ]]; then
    read -p "Write preferred scale factor (example: 1.25): "  SCALE_FACTOR
    line_append="--force-device-scale-factor=${SCALE_FACTOR} \\"
    echo $line_append >> $HOME/.xinitrc
  fi

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
