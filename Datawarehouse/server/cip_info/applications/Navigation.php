<?php

class Navigation {

  protected $uri;
  protected $environment;
  public $top_nav_links;

  function __construct () {
    $this->environment = new Environment();
    $this->uri = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->top_nav_links = array();
    $this->top_nav_links['Hjem'] = $this->uri ;
    $this->top_nav_links['Finn Vare'] = $this->uri . '/find';
    $this->top_nav_links['Plassering'] = $this->uri . '/placement';
    $this->top_nav_links['Rapporter'] = $this->uri . '/reports';
    $this->top_nav_links['Strekkoder'] = $this->uri . '/barcodes';
    $this->top_nav_links['Kart'] = $this->uri . '/map';
    $this->top_nav_links['Instrukser'] = $this->uri . '/instructions';
    $this->top_nav_links['Om'] = $this->uri . '/about';

    // show extra nav links in top menu for developer if enabled
    if ($this->environment->developement('show_nav_links')) {
      $this->top_nav_links['Devtools'] = $this->uri . '/developing';
      $this->top_nav_links['API'] = $this->uri . '/api';
      $this->top_nav_links['Example'] = $this->uri . '/example';
    }
  }

}
