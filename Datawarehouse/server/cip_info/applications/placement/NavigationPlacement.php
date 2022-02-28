<?php

require_once '../applications/Navigation.php';

class NavigationPlacement extends Navigation {

  public $sub_nav_links;
  protected $home_sub; // links to domain/find

  function __construct () {
    parent::__construct();
    $this->home_sub = $this->top_nav_links['Plassering'];
      $this->sub_nav_links = [
      'Legge Inn Vareplassering' => $this->home_sub . '/register',
      'Finn Vareplassering' => $this->home_sub . '/get',
    ];

  }
}
