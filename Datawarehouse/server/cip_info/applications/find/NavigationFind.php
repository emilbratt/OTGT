<?php

require_once '../applications/Navigation.php';

class NavigationFind extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Finn Vare'];
      $this->sub_nav_links = [
      'Søk Etter Vare' => $this->app_uri . '/bysearch',
      'Skann Vare' => $this->app_uri . '/bybarcode',
    ];
  }

}
