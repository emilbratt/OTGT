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

function _docker_compose_up () {
  _shout_out 'Starting services with "docker-compose up"'
  docker-compose up --no-deps --build || exit 1
}

function _show_container_info () {
  _shout_out 'Overview of running container'
  docker-compose ps
}

function _main () {
  _docker_compose_down
  _docker_compose_up
  _show_container_info
  _shout_out 'We are done!'
}

_main
