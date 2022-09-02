<?php

class Apprequest {

  private $app_dir;
  private $app_class;
  private $url_split;
  private $show_errors;

  function __construct ()  {
    $environment = new Environment();
    $this->show_errors = $environment->developement('show_errors');
    if ($this->show_errors) {
      ini_set('display_errors', 1);
      ini_set('display_startup_errors', 1);
      error_reporting(E_ALL);
    }
    unset ($environment);
  }

  public function run () {
    // store the URL into an array and use it to send client to correct app
    $this->url_split = explode('/', strtolower(substr($_SERVER['REDIRECT_URL'], 1)));

    // where the application is loaded by parsing url_split
    $this->load_app_dir();
    require_once "../applications/$this->app_dir/Application.php";

    // where we load the correct class inside appdirectory using url_split
    $this->load_app_class();

    // where the application is started
    $page = new $this->app_class;
    $page->run();
    // application is terminated, au revoir! :)
  }

  private function load_app_dir () {
    // set the default app dir and go from there..
    $this->app_dir = 'home';

    if ($_SERVER['REDIRECT_URL'] === '/') {
      return;
    }

    if ( isset($this->url_split[0]) ) {
      $this->app_dir = $this->url_split[0];
    }

    if ( is_dir("../applications/$this->app_dir") ) {
      return;
    }

    $this->app_dir = explode('&', $this->app_dir)[0];
    if ( is_dir("../applications/$this->app_dir") ) {
      return;
    }

    if ($this->show_errors) {
      echo "Directory: applications/$this->app_dir not found";
      http_response_code(404);
      exit(1);
    }

    // send the client to default app dir
    $this->app_dir = 'home';
  }

  private function load_app_class () {
    // set the default app class and go from there..
    $this->app_class = 'Home';

    if ($_SERVER['REDIRECT_URL'] === '/') {
      return;
    }

    if ( isset($this->url_split[1]) ) {
      $this->app_class = ucfirst($this->url_split[1]);
    }

    // load class in Application.php
    if ( class_exists($this->app_class) ) {
      return;
    }

    $this->app_class = explode('&', $this->url_split[1])[0];
    if ( class_exists($this->app_class) ) {
      return;
    }

    // at this point the class (app) was not found
    if ($this->show_errors) {
      echo "Class $this->app_class: " . $_SERVER['HTTP_HOST'] . "/$this->app_dir.php does not exist";
      http_response_code(404);
      exit(1);
    }

    // send the client to default class
    $this->app_class = 'Home';
  }

}
