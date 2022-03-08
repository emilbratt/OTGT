<?php

require_once '../applications/Navigation.php';

class NavigationReports extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Rapporter'];
      $this->sub_nav_links = [
      'Import' => $this->app_uri . '/imported',
      'Utsolgt' => $this->app_uri . '/soldout',
      'Salg' => $this->app_uri . '/sold',
    ];
  }

}
