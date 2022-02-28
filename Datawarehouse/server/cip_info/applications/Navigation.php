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
    $this->home_ = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'];
    $this->top_nav_links = [
      'Hjem' => $this->home_,
      'Vare' => $this->home_ . '/find',
      'Rapporter' => $this->home_ . '/reports',
      'Plassering' => $this->home_ . '/placement',
      'Kart' => $this->home_ . '/map',
    ];
  }

}
