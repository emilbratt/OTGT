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
    $this->top_nav_links = array();
    $this->top_nav_links['Hjem'] = $this->address ;
    $this->top_nav_links['Vare'] = $this->address . '/find';
    $this->top_nav_links['Rapporter'] = $this->address . '/reports';
    $this->top_nav_links['Kart'] = $this->address . '/map';
    $this->top_nav_links['Om'] = $this->address . '/about';

    if ($this->environment->developement('show_nav_links')) {
      // extra menu entries shown if environment set accordingly
      $this->top_nav_links['Plassering'] = $this->address . '/placement';
      $this->top_nav_links['Utvikling'] = $this->address . '/developing';
      $this->top_nav_links['Instrukser'] = $this->address . '/instructions';
    }
  }

}
