<?php

require_once '../applications/Navigation.php';

class NavigationPlacement extends Navigation {

  public $sub_nav_links;
  protected $app_uri;

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Plasser Vare'];
      $this->sub_nav_links = [
      'Legg inn med bruk av skanner' => $this->app_uri . '/scanitemscanshelf',
      // 'Finn Vareplassering' => $this->app_uri . '/getplacement',
    ];
  }

}
