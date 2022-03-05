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
  protected $template;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/placement/TemplatePlacement.php';
    require_once '../applications/placement/NavigationPlacement.php';

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
    $navigation = new NavigationPlacement();
    $this->template->top_navbar($navigation->top_nav_links, $this->page);
    $this->template->title('Plassering');
    $this->template->message('funksjon for å legge inn plassering etc. vil komme her');
    $this->template->print();
  }

}
