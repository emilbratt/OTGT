<?php

/*
 *
 * TODO;
 *  add: method for adding extra top nav links for developer tools (sql shell etc.)
 *
 */

class Navigation {

  public $top_nav_links;
  private $environment;
  protected $nav_links;
  protected $address; // links to: domain/

  function __construct ($environment) {
    $this->environment = $environment;
    $this->address = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->top_nav_links = [
      'Hjem' => $this->address,
      'Vare' => $this->address . '/find',
      'Rapporter' => $this->address . '/reports',
      'Plassering' => $this->address . '/placement',
      'Kart' => $this->address . '/map',
      'Om' => $this->address . '/about',
    ];

    if ($this->environment->developement('show_nav_links')) {
      // extra menu entries shown if environment set accordingly
      $this->top_nav_links['Utvikling'] = $this->address . '/developing';
      $this->top_nav_links['Instrukser'] = $this->address . '/instructions';
    }
  }

}
