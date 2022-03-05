<?php

require_once '../applications/Navigation.php';

class NavigationMap extends Navigation {

  function __construct () {
    parent::__construct();
    $this->home_sub = $this->top_nav_links['Kart'];
      $this->sub_nav_links = [
      '1 etg.' => $this->home_sub . '/floor_1',
      'U etg.' => $this->home_sub . '/floor_U',
      'U1 etg.' => $this->home_sub . '/floor_U1',
    ];
  }

}
