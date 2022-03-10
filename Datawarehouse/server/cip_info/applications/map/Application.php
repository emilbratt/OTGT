<?php

class Map {

  protected $page = 'Kart'; // alias for top_navbar
  protected $environment;
  protected $template;
  protected $navigation;

  function __construct () {
    require_once '../applications/Helpers.php';
    require_once '../applications/map/TemplateMap.php';
    require_once '../applications/map/NavigationMap.php';

    $this->environment = new Environment();
    $this->navigation = new NavigationMap();
    $this->template = new TemplateMap();
    $this->template->top_navbar($this->navigation->top_nav_links, $this->page);
  }

}


class Home extends Map {

  public function run () {
    $this->template->sub_navbar($this->navigation->sub_nav_links);
    $this->template->map_form_location();
    if (isset($_GET['input_field_location'])) {
      $this->template->image_location();
    }
    $this->template->print();
  }

}


class floor_1 extends Map {

  public function run () {
    $this->template->image_map('1');
    $this->template->print();
  }

}


class floor_U extends Map {

  public function run () {
    $this->template->image_map('U');
    $this->template->print();
  }

}

class floor_U1 extends Map {

  public function run () {
    $this->template->image_map('U1');
    $this->template->print();
  }

}
