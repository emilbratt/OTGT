<?php

require_once '../applications/Navigation.php';

class NavigationReports extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Rapporter'];
      $this->sub_nav_links = [
      'Varer som har kommet inn' => $this->app_uri . '/imported',
      'Utsolgte varer' => $this->app_uri . '/soldout',
      'Alle Salg' => $this->app_uri . '/sold',
    ];
  }

}
