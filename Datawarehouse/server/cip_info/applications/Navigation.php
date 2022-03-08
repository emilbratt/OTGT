<?php

/*
 *
 * TODO;
 *  add: method for adding extra top nav links for developer tools (sql shell etc.)
 *
 */

class Navigation {

  protected $uri;
  protected $environment;
  public $top_nav_links;

  function __construct () {
    $this->environment = new Environment();
    $this->uri = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->top_nav_links = array();
    $this->top_nav_links['Hjem'] = $this->uri ;
    $this->top_nav_links['Vare'] = $this->uri . '/find';
    $this->top_nav_links['Rapporter'] = $this->uri . '/reports';
    $this->top_nav_links['Kart'] = $this->uri . '/map';
    $this->top_nav_links['Om'] = $this->uri . '/about';

    if ($this->environment->developement('show_nav_links')) {
      // extra menu entries shown if environment set accordingly
      $this->top_nav_links['Plassering'] = $this->uri . '/placement';
      $this->top_nav_links['Utvikling'] = $this->uri . '/developing';
      $this->top_nav_links['Instrukser'] = $this->uri . '/instructions';
    }
  }

}
