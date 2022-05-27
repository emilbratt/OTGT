<?php

require_once '../applications/Navigation.php';

class NavigationInstructions extends Navigation {

  function __construct () {
    parent::__construct();
    $this->app_uri = $this->top_nav_links['Instrukser'];
  }

}
