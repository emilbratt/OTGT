<?php

require_once '../applications/Navigation.php';

class NavigationMap extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Kart'];
      $this->sub_nav_links = [
      '1 etg.' => $this->app_uri . '/floor_1',
      'U etg.' => $this->app_uri . '/floor_U',
      'U1 etg.' => $this->app_uri . '/floor_U1',
    ];
  }

}
