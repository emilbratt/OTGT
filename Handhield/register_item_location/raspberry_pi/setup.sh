#!/usr/bin/env bash
#────────────────────────────────────────────#
# Author:
#   Emil Bratt Børsting
#────────────────────────────────────────────#
# Description:
#   automatically setup handhield running script
#   for the item locatin register 'interface
#────────────────────────────────────────────#

declare PYTHON_CODE
declare PYTHON_MODULES
declare INTERFACE_EXECUTABLE

INTERFACE_EXECUTABLE="OTGT/Handhield/register_item_location/raspberry_pi/application/interface.py"

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


function get_python_pip () {
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


function install_application () {
  sudo cp register-item-location-d.service /etc/systemd/system/
  sudo systemctl enable register-item-location-d
  cat $HOME/.bashrc | grep -q "$HOME/$INTERFACE_EXECUTABLE"
  if [[ $? -eq 1 ]]; then
    echo "$HOME/$INTERFACE_EXECUTABLE" >> $HOME/.bashrc
  fi

  if [[ ! -f $HOME/OTGT/environment.ini ]]; then
    echo "API Host:"
    read host
    echo "API Port"
    read port
    echo "[datawarehouse]" > $HOME/OTGT/environment.ini
    echo "cip_info_host = $host" >> $HOME/OTGT/environment.ini
    echo "cip_info_port = $port" >> $HOME/OTGT/environment.ini
  fi
}


check_internet_connection
setup_hostname
system_update
get_python_pip
install_python_modules
install_application

echo 'Press Enter to reboot'
read
sudo reboot
