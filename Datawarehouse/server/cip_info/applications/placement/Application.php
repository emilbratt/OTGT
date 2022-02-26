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
  protected $template;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/placement/TemplatePlacement.php';
    require_once '../applications/placement/NavigationPlacement.php';
    // html starts here
    $this->template = new TemplatePlacement();
    $this->template->start();

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
    $this->template->top_navbar($navigation->top_nav_links);
    $this->template->title('Plassering');
    $this->template->print();
  }

}
