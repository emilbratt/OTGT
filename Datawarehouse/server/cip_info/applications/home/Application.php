<?php

class Home {

  protected $page;

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Helpers.php';
    require_once '../applications/home/TemplateHome.php';
    require_once '../applications/Navigation.php';
    $this->page = 'Hjem';
    $this->template = new TemplateHome();
    $this->template->start();
  }

  public function run () {

    $navigation = new Navigation();
    $this->template->top_navbar($navigation->top_nav_links, $this->page);
    $this->template->title('Hjem');
    $this->template->print();
  }

}
