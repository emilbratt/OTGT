<?php

/*
 *
 * simple way to create navigation links
 *
 */

class Navigation {

  public $top_nav_links;
  protected $nav_links;
  protected $home_address; // example: http://hostname:8080

  function __construct () {
    $this->home_address =  $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->top_nav_links = [
      'Hjem' => $this->home_address . '/home/home',
      'Søk' => $this->home_address . '/find',
      'Rapporter' => $this->home_address . '/reports',
      'Plassering' => $this->home_address . '/placement',
      'Kart' => $this->home_address . '/map',
    ];
  }

}
