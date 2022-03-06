<?php

require_once '../applications/Navigation.php';

class NavigationReports extends Navigation {

  function __construct ($environment) {
    parent::__construct($environment);
    $this->home_sub = $this->top_nav_links['Rapporter'];
      $this->sub_nav_links = [
      'Import' => $this->home_sub . '/imported',
      'Utsolgt' => $this->home_sub . '/soldout',
      'Salg' => $this->home_sub . '/sold',
    ];
  }

}
