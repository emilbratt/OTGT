<?php

/**
 *
 * TODO:
 *  add: quick input box for barcode scanning
 *  add: overview over todays turnover with diagram
 *  add: pick our todays seller based in random choice (not based on most sales etc.)
 *
 */

class Home {

  protected $page = 'Hjem';
  protected $environment;
  protected $navigation;
  protected $title_left;
  protected $title_right;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/home/TemplateHome.php';
    require_once '../applications/Navigation.php';

    $this->environment = new Environment();
    $this->template = new TemplateHome();
    $this->navigation = new Navigation();

    $this->title_left = 'C.I.Pedersen';
    $this->title_right = Dates::get_this_weekday() . ' ' . date("d/m-Y");


    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

  public function run () {
    $this->template->title_left_and_right($this->title_left, $this->title_right);
    $this->template->print();
  }

}
