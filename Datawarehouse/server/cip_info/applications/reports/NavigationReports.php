<?php

require_once '../applications/Navigation.php';

class NavigationReports extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Rapporter'];
      $this->sub_nav_links = [
      'Varemottak' => $this->app_uri . '/imported',
      'Utsolgte varer' => $this->app_uri . '/soldout',
      'Alle Salg' => $this->app_uri . '/saleshistory',
      'Ikke solgt på lenge' => $this->app_uri . '/notsoldlately',
      'Salg pr. time' => $this->app_uri . '/salesperhour',
      'Merke' => $this->app_uri . '/brand',
    ];
  }

}
