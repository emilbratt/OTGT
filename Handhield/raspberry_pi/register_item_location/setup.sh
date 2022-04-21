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
declare PYTHON_CODE
declare PYTHON_MODULES

DEPENDENCIES=(
  # shelf-daemon.service
  wifisignal
  application/main.py
)

PYTHON_MODULES=(
  requests
)


# python code checking if a module passed as arg is installed and exits accordingly with 0 or 1
read -r -d '' PYTHON_CODE <<- EOT
import sys
import importlib
try:
  importlib.import_module(sys.argv[1], package=None)
  sys.exit(0)
except ModuleNotFoundError:
  sys.exit(1)
EOT


function check_dependencies () {
  path=$(pwd)
  for file in "${DEPENDENCIES[@]}"
  do
    path="$path/$file"
    echo "Checking existens of $path"
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
  sudo apt-get install python3-pip -y
}


function install_python_modules () {
  for module in "${PYTHON_MODULES[@]}"
  do
    echo "Checking if Python $module is installed"
    python3 -c "$PYTHON_CODE" $module
    if [[ $? -ne 0 ]]; then
      pip3 install --user $module
    fi
  done
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
# system_update
# setup_software
install_python_modules
# check_internet_connection
# setup_hostname
# set_locale
# install_dependencies
# sudo reboot
