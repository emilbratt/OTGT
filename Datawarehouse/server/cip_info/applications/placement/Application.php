<?php

/**
 *
 * TODO:
 * register by scanning item, then scanning shelf
 * on screen verification should be implemented
 *
 */


class Register {
  // shows reports of soldout items for today, this week or this month
  protected $page = 'Plassering'; // alias for top_navbar
  protected $environment;
  protected $template;
  protected $navigation;

  function __construct () {
    require_once '../applications/Environment.php';
    require_once '../applications/Helpers.php';
    require_once '../applications/placement/TemplatePlacement.php';
    require_once '../applications/placement/NavigationPlacement.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationPlacement($this->environment);
    $this->template = new TemplatePlacement();
  }

}


class Home extends Register {

  public function run () {
    if(UserAgent::is_mobile()) {
      // if on mobile
    }
    else {
      // if on desktop;
    }

    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
    $this->template->title('Plassering');
    $this->template->message('funksjon for å legge inn plassering etc. vil komme her');
    $this->template->print();
  }

}
