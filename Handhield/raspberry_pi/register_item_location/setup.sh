#!/usr/bin/env bash
#────────────────────────────────────────────#
# Author:
#   Emil Bratt Børsting
#────────────────────────────────────────────#
# Description:
#   automatically setup handhield running script
#   for registering item shelf value
#────────────────────────────────────────────#
# Customization of this script
#   add dependencies (files) and make sure they
#   are listed in the DEPENDENCIES variable
#────────────────────────────────────────────#

declare DEPENDENCIES

DEPENDENCIES=(
  shelf-daemon.service
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
  sudo apt-get update && sudo apt-get upgrade -y
}


function setup_software () {
  return 0
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


function install_dependencies () {
  return 0
}


check_dependencies
check_internet_connection
setup_hostname
system_update
setup_software
set_locale
install_dependencies
sudo reboot
