<?php

require_once '../applications/Navigation.php';

class NavigationFind extends Navigation {

  public $sub_nav_links;
  protected $home_sub; // links to domain/find

  function __construct () {
    parent::__construct();
    $this->home_sub = $this->top_nav_links['Vare'];
      $this->sub_nav_links = [
      'Søk Etter Vare' => $this->home_sub . '/bysearch',
      'Skann Vare' => $this->home_sub . '/bybarcode',
    ];
  }
}
