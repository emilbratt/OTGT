#!/usr/bin/env bash

# Description:
#   run the script from the same directory e.g. $ ./setup.sh
#
#   this script will prepare the basic configuration needed
#   for the docker-compose.yml file to work properly
#
#   it is meant to be used as a developement instance to
#   spin up the container from inside this repo without hassle

# for bind-mount
HOST_BIND_MOUNT_DIRECTORY=./bindmount
mkdir -p $HOST_BIND_MOUNT_DIRECTORY

# default configurations (these will be possible to change during run-time)
PORT=1883
DATA_PERSISTANCE=true
PERSISTENCE_LOCATION=/mosquitto/data
LOG_FILE=/mosquitto/log/mosquitto.log
ALLOW_ANONYMOUS=false
PASSWORD_FILE=/mosquitto/config/password.txt

function _shout_out () {
  echo ''
  echo '###'
  echo '###' ${1}
  echo '###'
  echo ''
  echo 'Press Enter to continue..'
  read
}

function _docker_compose_down () {
  _shout_out 'Stopping container if running, ignore warnings'
  docker-compose down || exit 1
}

function _generate_config () {
  host_config_directory=${HOST_BIND_MOUNT_DIRECTORY}/config
  host_config_file=${HOST_BIND_MOUNT_DIRECTORY}/config/mosquitto.conf
  host_password_file=${HOST_BIND_MOUNT_DIRECTORY}/config/password.txt

  host_log_directory=${HOST_BIND_MOUNT_DIRECTORY}/log

  host_data_directory=${HOST_BIND_MOUNT_DIRECTORY}/data

  _shout_out 'IMPORTANT! This setup will over-write existing configs and password (CTRL-C to exit)'

  mkdir -p $host_config_directory
  rm -f $host_config_file && touch $host_config_file
  rm -f $host_password_file && touch $host_password_file

  mkdir -p $host_log_directory
  chmod 777 $host_log_directory || exit 1

  mkdir -p $host_data_directory
  chmod 777 $host_data_directory || exit 1

  _shout_out 'Unless you know what you are doing, use the defaults'

  echo 'Listener Port (use backspace to change value)'
  read -e -i ${PORT} -p '' input
  config_line_1="listener ${input:-$PORT}"

  echo 'Persist data (use backspace to change value)'
  read -e -i ${DATA_PERSISTANCE} -p '' input
  config_line_2="persistence ${input:-$DATA_PERSISTANCE}"

  echo 'Persist data location (use backspace to change value)'
  read -e -i ${PERSISTENCE_LOCATION} -p '' input
  config_line_3="persistence_location ${input:-$PERSISTENCE_LOCATION}"

  echo 'Set log file path (use backspace to change value)'
  read -e -i ${LOG_FILE} -p '' input
  config_line_4="log_dest file ${input:-$LOG_FILE}"

  echo 'Allow un-authenticated (anonymous) connection (use backspace to change value)'
  read -e -i ${ALLOW_ANONYMOUS} -p '' input
  config_line_5="allow_anonymous ${input:-$ALLOW_ANONYMOUS}"

  echo 'Password file path (use backspace to change value)'
  read -e -i ${PASSWORD_FILE} -p '' input
  config_line_6="password_file ${input:-$PASSWORD_FILE}"

  _shout_out "Saving config parameters and values to ${host_config_file}"

  echo '### Current configuration to be written ###'
  echo $config_line_1 | tee -a $host_config_file
  echo $config_line_2 | tee -a $host_config_file
  echo $config_line_3 | tee -a $host_config_file
  echo $config_line_4 | tee -a $host_config_file
  echo $config_line_5 | tee -a $host_config_file
  echo $config_line_6 | tee -a $host_config_file
}

function _docker_compose_up () {
  _shout_out 'Starting mosquitto container with "docker-compose up"'
  docker-compose up -d || exit 1
}

function _add_password () {
  _shout_out 'Set a user and (for the love of god) a strong password for authorising MQTT connections'
  printf 'User: ' ; read user
  read -s -p "Password: " password; echo ''
  docker-compose exec mosquitto mosquitto_passwd -b $PASSWORD_FILE $user $password || exit 1
}

 function _docker_compose_restart () {
   _shout_out 'Restarting mosquitto with new password settings'
   docker-compose restart || exit 1
}

function _show_container_info () {
  _shout_out 'Overview of running container'
  docker-compose ps
}

function _main () {
  _docker_compose_down
  _generate_config
  _docker_compose_up
  _add_password
  _docker_compose_restart
  _show_container_info
  _shout_out 'We are done!'
}

_main
