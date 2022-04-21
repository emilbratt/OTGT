<?php

/**
 *
 * NOTE:
 *  remember to add new methods for any new corresponding section
 *  that is added in environment.ini
 *
 *  keep in mind that the environment.ini file is globally used as
 *  across the repository and such is also used by applications
 *  not related to this web-server
 *
 */

class Environment {

  protected $env_file_path;
  public $env_config;

  function __construct () {
    $this->env_file_path = '../../../../environment.ini';
    $this->env_config = parse_ini_file($this->env_file_path, $process_sections = true);
  }

  public function retail ($key) {
    return $this->env_config['retail'][$key];
  }

  public function datawarehouse ($key) {
    return $this->env_config['datawarehouse'][$key];
  }

  public function nextcloud_otgt ($key) {
    return $this->env_config['nextcloud_otgt'][$key];
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
