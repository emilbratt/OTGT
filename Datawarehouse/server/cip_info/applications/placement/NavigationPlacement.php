<?php

require_once '../applications/Navigation.php';

class NavigationPlacement extends Navigation {

  public $sub_nav_links;
  protected $home_sub; // links to domain/find

  function __construct ($environment) {
    parent::__construct($environment);
    $this->home_sub = $this->top_nav_links['Plassering'];
      $this->sub_nav_links = [
      'Legg inn med bruk av skanner' => $this->home_sub . '/scanitemscanshelf',
      // 'Finn Vareplassering' => $this->home_sub . '/getplacement',
    ];
  }

}
