<?php

class Apprequest {

  protected $app_dir;
  protected $app_class;
  private $url_split;
  private $show_errors;

  function __construct ()  {
    $config_file = '../../../../environment.ini';
    $config = parse_ini_file($config_file, $process_sections = true);
    $this->show_errors = $config['developement']['show_errors'];

    $this->load_directory();
    require_once "../applications/$this->app_dir/Application.php";
    $this->load_class();
    $app = new $this->app_class;
    $app->run();
  }

  private function load_directory () {
    // the 1st word in the url = app directory which resides in ../applications
    // defaults that is changed if specified in URL
    if($_SERVER['REDIRECT_URL'] === '/') {
      $this->app_dir = 'home';
      return;
    }

    $this->url_split = explode('/', strtolower(substr($_SERVER['REDIRECT_URL'], 1)));
    if (isset($this->url_split[0])) {
      $this->app_dir = $this->url_split[0];
    }

    if (is_dir("../applications/$this->app_dir")) {
      return;
    }

    $this->app_dir = explode('&', $this->app_dir)[0];
    if(is_dir("../applications/$this->app_dir")) {
      return;
    }

    if ($this->show_errors) {
      echo "Directory: " . $_SERVER['HTTP_HOST'] . "/$this->app_dir not found";
    }
    http_response_code(404);
    exit(1);
  }

  private function load_class () {
    // the 2nd word in the url = app class which is loaded in Application.php
    if($_SERVER['REDIRECT_URL'] === '/') {
      $this->app_class = 'Home';
      return;
    }

    $this->app_class = 'Home';
    if (isset($this->url_split[1])) {
      $this->app_class = ucfirst($this->url_split[1]);
    }

    // load class in Application.php
    if (class_exists($this->app_class)) {
      return;
    }

    $this->app_class = explode('&', $this->url_split[1])[0];
    if(class_exists($this->app_class)) {
      return;
    }

    // at this point the class was not found
    if ($this->show_errors) {
      echo "Class $this->app_class: " . $_SERVER['HTTP_HOST'] . "/$this->app_dir.php does not exist";
    }
    http_response_code(404);
    exit(1);
    }

}
