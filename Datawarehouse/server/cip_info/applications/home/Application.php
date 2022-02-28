<?php

class Home {

  protected $page = 'Hjem';

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Helpers.php';
    require_once '../applications/home/TemplateHome.php';
    require_once '../applications/Navigation.php';

    $this->template = new TemplateHome();
    $navigation = new Navigation();
    $this->template->start();
    $this->template->top_navbar($navigation->top_nav_links, $this->page);
  }

  public function run () {
    $this->template->title('Hjem');
    $this->template->print();
  }

}
