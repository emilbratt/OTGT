<?php


class Map {

  protected $page;
  protected $template;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/map/TemplateMap.php';
    require_once '../applications/map/NavigationMap.php';
    $this->page = 'Kart';
    $this->template = new TemplateMap();
    $this->template->start();

  }
}


class Home extends Map {

  public function run () {
    if(UserAgent::is_mobile()) {
      // if on mobile
    }
    else {
      // if on desktop;
    }
    $navigation = new NavigationMap();
    $this->template->top_navbar($navigation->top_nav_links, $this->page);
    $this->template->title('Kart');
    $this->template->print();
  }

}
