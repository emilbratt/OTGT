<?php

/**
 *
 * add: quick input box for barcode scanning
 * add: overview over todays turnover
 * add: diagram
 *
 */

class Home {

  protected $page = 'Hjem';

  function __construct () {
    // shows reports of soldout items for today, this week or this month
    require_once '../applications/Helpers.php';
    require_once '../applications/home/TemplateHome.php';
    require_once '../applications/Navigation.php';

    $this->template = new TemplateHome();
    $navigation = new Navigation();
    $this->template->top_navbar($navigation->top_nav_links, $this->page);
  }

  public function run () {
    $this->template->title('C.I.Pedersen Trondheim');
    $this->template->message('Velg fra toppmenyen');
    $this->template->print();
  }

}
