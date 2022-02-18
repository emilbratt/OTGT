<?php

class Apprequest {

  protected $app_dir;
  protected $app_class;

  function __construct ()  {
    $this->parse_url();
    $this->load_app();
  }


  private function parse_url () {
    // defaults that is changed if specified in URL
    $this->app_class = 'Home';
    if($_SERVER['REDIRECT_URL'] === '/') {
      $this->app_dir = 'home';
      return;
    }
    $url_split = explode('/', strtolower(substr($_SERVER['REDIRECT_URL'], 1)));
    if (isset($url_split[0])) {
      $this->app_dir = $url_split[0];
    }

    if (!(is_dir("./applications/$this->app_dir"))) {
      $this->app_dir = explode('&', $this->app_dir)[0];
      if(!(is_dir("./applications/$this->app_dir"))) {
        echo "Directory: " . $_SERVER['HTTP_HOST'] . "/$this->app_dir not found";
        http_response_code(404);
        exit(1);
      }
    }

    if (isset($url_split[1])) {
      $this->app_class = ucfirst($url_split[1]);
    }
  }

  private function load_app () {
    // load Application.php inside the appapplications directory
    if (!(is_dir("./applications/$this->app_dir"))) {
      echo "Directory: " . $_SERVER['HTTP_HOST'] . "/$this->app_dir not found" ;
      http_response_code(404);
      exit(1);
    }
    require_once "./applications/$this->app_dir/Application.php";

    // load class in Application.php
    if (class_exists($this->app_class)) {
      $app = new $this->app_class;
      return;
    }
    echo "Class $this->app_class: " . $_SERVER['HTTP_HOST'] . "/$this->app_dir.php does not exist" ;
    http_response_code(404);
    exit(1);
  }

}


class Pagerequest {
  // if needed by the classes in ./applications/<app> to route request to correct file
  public static function get_file ($page_directory) {
    $url_split = explode('/', strtolower(substr($_SERVER['REDIRECT_URL'], 1)));
    if (isset($url_split[2])) {
      $page = $page_directory . '/' . $url_split[2] . '.php';
      // should work if no "&" (GET array) after url
      if(is_file($page)) {
        return $page;
      }

      // if there is a "&" (GET array) after url
      $page = explode('&', $page)[0] . '.php';
      if(is_file($page)) {
        return $page;
      }

      // if none of the above, send 404
      echo "File: " . $_SERVER['HTTP_HOST'] . "$page not found" ;
      http_response_code(404);
      exit(1);
    }
    return false;
  }
}
