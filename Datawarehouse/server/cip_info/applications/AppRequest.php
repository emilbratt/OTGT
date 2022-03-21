<?php

class Apprequest {

  protected $app_dir;
  protected $app_class;
  private $url_split;
  private $show_errors;

  function __construct ()  {
    require_once '../applications/Environment.php';
    $environment = new Environment();
    $this->show_errors = $environment->developement('show_errors');
    if ($this->show_errors) {
      ini_set('display_errors', 1);
      ini_set('display_startup_errors', 1);
      error_reporting(E_ALL);
    }
    unset ($environment);

    // this is where the application is loaded and instantiated based on URI
    $this->load_app_dir();
    require_once "../applications/$this->app_dir/Application.php";
    $this->load_app_class();
    $app = new $this->app_class;
    $app->run();
    // atthis point the app has terminated and the script is done
  }

  private function load_app_dir () {
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
      echo "Directory: applications/$this->app_dir not found";
    }
    http_response_code(404);
    exit(1);
  }

  private function load_app_class () {
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
