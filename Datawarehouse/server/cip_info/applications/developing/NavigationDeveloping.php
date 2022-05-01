<?php

require_once '../applications/Navigation.php';

class NavigationDeveloping extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Devtools'];
      $this->sub_nav_links = [
      'SQL Shell Retail' => $this->app_uri . '/sqlshellretail',
      'SQL Shell Datawarehouse' => $this->app_uri . '/sqlshelldatawarehouse',
      'Performance' => $this->app_uri . '/performance',
      'Get Shelf Label Dummy Sheet' => $this->app_uri . '/generatelabeldummysheet',
      'Memory Database' => $this->app_uri . '/memorydatabase',

    ];
  }

}
