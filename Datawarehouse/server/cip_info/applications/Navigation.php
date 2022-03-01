<?php

/*
 *
 * simple way to create navigation links
 * these are links that are hard-coded
 *
 */

class Navigation {

  public $top_nav_links;
  protected $nav_links;
  protected $home; // links to: domain/

  function __construct () {
    $this->home = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->top_nav_links = [
      'Hjem' => $this->home,
      'Vare' => $this->home . '/find',
      'Rapporter' => $this->home . '/reports',
      'Plassering' => $this->home . '/placement',
      'Kart' => $this->home . '/map',
      'Instrukser' => $this->home . '/instructions',
    ];
  }

}
