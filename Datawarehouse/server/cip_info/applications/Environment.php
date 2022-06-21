<?php

/**
 *
 * NOTE:
 *  remember to add new methods for any new corresponding section
 *  that is added in environment.ini
 *
 *  keep in mind that the environment.ini file is globally
 *  used as across the repository including applications
 *  not related to this web-server
 *
 */

class Environment {

  private $env_config;

  function __construct () {
    $this->env_config = parse_ini_file(ENVIRONMENT_INI, $process_sections = true);
  }

  public function assets ($key) {
    return $this->env_config['assets'][$key];
  }

  public function retail ($key) {
    return $this->env_config['retail'][$key];
  }

  public function datawarehouse ($key) {
    return $this->env_config['datawarehouse'][$key];
  }

  public function cloudstorage ($key) {
    return $this->env_config['cloudstorage'][$key];
  }

  public function developement ($key) {
    return $this->env_config['developement'][$key];
  }

  public function contact_dev ($key) {
    return $this->env_config['contact_dev'][$key];
  }

  public function contact_staff ($key) {
    return $this->env_config['contact_staff'][$key];
  }

  public function contact_sysadmin ($key) {
    return $this->env_config['contact_sysadmin'][$key];
  }

  public function confidential ($key) {
    return $this->env_config['confidential'][$key];
  }

  public function competitive ($key) {
    return $this->env_config['competitive'][$key];
  }

  function __destruct () {

  }

}
