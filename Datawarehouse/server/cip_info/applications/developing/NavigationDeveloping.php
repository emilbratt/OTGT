<?php

require_once '../applications/Navigation.php';

class NavigationDeveloping extends Navigation {

  function __construct ($environment) {
    parent::__construct($environment);
    $this->home_sub = $this->top_nav_links['Utvikling'];
      $this->sub_nav_links = [
      'SQL Shell' => $this->home_sub . '/sqlshell',
      'API' => $this->home_sub . '/api',
      'Testing' => $this->home_sub . '/testing',
    ];
  }

}
