<?php

require_once '../applications/Navigation.php';

class NavigationPlacement extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
  }

}
