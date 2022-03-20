<?php

class API {

  protected $page = 'Api'; // REMEMBER TO ADD THIS PAGE NAME SO THE CORRECT TOP MENU BAR IS HIGHLIGHET
  protected $environment;

  function __construct () {
    $this->environment = new Environment();

  }

}


class Home extends API {

  public function run () {
    echo 'api ok';
  }

}
